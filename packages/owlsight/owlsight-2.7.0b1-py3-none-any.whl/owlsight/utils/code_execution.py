import os
import re
from typing import Dict, List, Union
import traceback
import inspect
from pathlib import Path

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.completion import WordCompleter

from owlsight.processors.text_generation_manager import TextGenerationManager
from owlsight.ui.constants import EDIT_CODE_BLOCK_COLOR
from owlsight.utils.custom_exceptions import ModuleNotFoundInVenvError
from owlsight.utils.custom_classes import GlobalPythonVarsDict
from owlsight.utils.subprocess_utils import execute_shell_command
from owlsight.utils.helper_functions import (
    parse_markdown,
    editable_input,
    format_error_message,
    format_chat_history_as_string,
)
from owlsight.ui.console import get_user_choice
from owlsight.utils.venv_manager import (
    install_python_modules,
    get_lib_path,
    get_python_executable,
)
from owlsight.utils.constants import get_py_cache, KB_AUTOCOMPLETE
from owlsight.utils.logger import logger


class CodeExecutor:
    def __init__(
        self,
        manager: TextGenerationManager,
        pyenv_path: str,
        pip_path: str,
        temp_dir: str,
        python_compile_mode: str = "exec",
    ):
        """
        Initialize CodeExecutor.

        Parameters:
        ----------
        manager : TextGenerationManager
            The TextGenerationManager instance.
        pyenv_path : str
            The path to the Python environment.
        pip_path : str
            The path to the pip executable.
        temp_dir : str
            The temporary directory for code execution.
        python_compile_mode : str
            The compilation mode for code execution. Defaults to 'exec'.
            The mode must be 'exec' to compile a module, 'single' to compile a
            single (interactive) statement, or 'eval' to compile an expression.
        """
        self._validate_python_compile_mode(python_compile_mode)

        self.manager = manager
        self.temp_dir = temp_dir
        self.globals_dict = GlobalPythonVarsDict()
        self._attempts = 0
        self.python_compile_mode = python_compile_mode

        self._init_python_properties(pyenv_path, pip_path)
        self._fill_globals_dict()

    def execute_and_retry(
        self, lang: str, code_block: str, original_question: str, prompt_retry_on_error: bool = False
    ) -> bool:
        """
        Execute code block in the specified language and retry if an error occurs.
        """
        self._attempts = 0
        while self.retries_left > 0:
            logger.info(f"Executing {lang.capitalize()} code (Attempt {self._get_nth_attempt()}/{self.max_retries})...")
            try:
                self.execute_code_block(lang, code_block)
                logger.info(f"Code executed on attempt {self._get_nth_attempt()}.")
                return True
            except Exception as e:
                self._attempts += 1
                if self.retries_left > 0:
                    logger.warning(f"Error on attempt {self._attempts}: {e}")
                    logger.info(f"Retrying... ({self._get_nth_attempt()}/{self.max_retries})")
                    response_with_fixed_code = self._generate_fixed_code_response(
                        original_question, code_block, format_error_message(e)
                    )
                    extracted_code_blocks = parse_markdown(response_with_fixed_code)
                    if extracted_code_blocks:
                        code_block = extracted_code_blocks[-1][1]  # Use the LAST extracted block of code
                        logger.info(
                            f"Extracted last code block from response with a total of {len(extracted_code_blocks)} blocks."
                        )
                        if prompt_retry_on_error:
                            code_block = prompt_code_edit(code_block)
                            user_choice = get_user_choice(
                                {
                                    "Execute code": None,
                                    "Skip code": None,
                                }
                            )
                            if user_choice == "Skip code":
                                return False  # Exit early if the user chooses to skip the code
                        continue  # Retry execution with the updated code block
                    else:
                        logger.error(
                            "No code block could be extracted from the response. Probably the response didnt insert the code block correctly in markdown format."
                        )
                        return False
                else:
                    logger.error(f"Failed to execute {lang} code after {self.max_retries} attempts.")

        return False

    def execute_code_block(self, lang: str, code_block: str) -> None:
        if lang.lower() in ["python", "py"]:
            self.execute_python_code(code_block)
        elif lang.lower() in ["cmd", "bash", "shell"]:
            if "pip install" in code_block:
                modules_to_install = code_block.split("pip install")[1].strip()
                logger.info(
                    f"pip install found in command '{code_block}'. Installing module {modules_to_install} to target directory {self.temp_dir}"
                )
                self.pip_install(modules_to_install)
            else:
                execute_shell_command(code_block, self.pyenv_path)
        else:
            raise ValueError(f"Unsupported language: {lang}")

    def execute_python_code(self, code_block: str) -> None:
        """Execute Python code block."""
        try:
            exec(code_block, self.globals_dict)
        except ModuleNotFoundError as e:
            logger.error(f"Module not found: {e}")
            missing_module = extract_missing_module(str(e))
            module_is_installed = self.pip_install(missing_module)
            if module_is_installed:
                if missing_module not in os.listdir(self.temp_dir):
                    raise ModuleNotFoundInVenvError(
                        missing_module,
                        self.pyenv_path,
                        os.listdir(self.temp_dir),
                    )
                logger.info(f"Retrying execution after installing {missing_module}")
                self.execute_python_code(code_block)  # Retry execution
            else:
                logger.error(f"Failed to install {missing_module}. Cannot execute the code.")
        except Exception as e:
            logger.error(f"Error executing code: {traceback.format_exc()}")
            raise e

    def init_interactive_py_console(self) -> None:
        """Initialize an interactive Python console with enhanced capabilities."""
        namespace = self.globals_dict

        # Create key bindings to use Tab for autocompletion
        bindings = KeyBindings()

        @bindings.add("tab")
        def _(event):
            """Provide autocompletion from history on Tab key press."""
            buff = event.app.current_buffer

            if buff.complete_state is not None:
                # If there is an active completion, continue with the next suggestion
                buff.complete_next()
            else:
                # Start cycling through history if no completion is active
                if buff.history:
                    history_strings = buff.history.get_strings()  # Get all commands from history
                    current_input = buff.text

                    # Find the next command from history that starts with the current input
                    suggestions = [cmd for cmd in history_strings if cmd.startswith(current_input)]

                    if suggestions:
                        # If we have suggestions, set the buffer text to the last matching suggestion
                        buff.text = suggestions[-1]
                        buff.cursor_position = len(buff.text)

        @bindings.add(*KB_AUTOCOMPLETE)
        def _(event):
            "Initialize autocompletion, or select the next completion."
            buff = event.app.current_buffer
            if buff.complete_state:
                buff.complete_next()
            else:
                buff.start_completion(select_first=False)

        @bindings.add("c-a")  # Ctrl+A
        def _(event):
            """Select all text in the current buffer."""
            buff = event.app.current_buffer
            buff.cursor_position = len(buff.text)
            buff.start_selection()
            buff.cursor_position = 0

        @bindings.add("c-v")  # Ctrl+V
        def _(event):
            """Copy selected text to clipboard."""
            buff = event.app.current_buffer
            if buff.selection_state:
                data = buff.copy_selection()
                event.app.clipboard.set_data(data)

        @bindings.add("c-y")  # Ctrl+Y
        def _(event):
            """Paste text from clipboard."""
            buff = event.app.current_buffer
            buff.paste_clipboard_data(event.app.clipboard.get_data())

        global_vars = self.globals_dict.get_public_keys()

        session = PromptSession(
            history=FileHistory(self.python_interpreter_history_file),
            auto_suggest=AutoSuggestFromHistory(),
            enable_history_search=True,
            complete_while_typing=True,
            key_bindings=bindings,
            completer=WordCompleter(global_vars),
        )

        # Start REPL loop
        print(
            "Interactive Python interpreter activated.\n"
            "- Use up/down arrows to navigate command history\n"
            "- Use Tab for auto-completion\n"
            "- Use Escape+V for variable completion\n"
            "- Use Ctrl+A to select all\n"
            "- Use Ctrl+V to copy\n"
            "- Use Ctrl+Y to paste\n"
            "- Use `owl_show()` to show all active objects\n"
            "Type 'exit()' to quit the console."
        )

        while True:
            try:
                text = session.prompt(">>> ", key_bindings=bindings)
                if text.strip() == "exit()":
                    break
                else:
                    try:
                        code_obj = compile(text, "<stdin>", self.python_compile_mode)
                        exec(code_obj, namespace)
                    except Exception:
                        print(traceback.format_exc())
            except KeyboardInterrupt:
                # Handle Ctrl+C
                print("KeyboardInterrupt")
            except EOFError:
                # Handle Ctrl+D
                break
        print("Exiting interactive python console.")

    def pip_install(self, modules: str) -> bool:
        """Install Python modules using pip."""
        logger.info(f"Attempting to install modules: {modules}")
        extra_index_url = self.manager.get_config_key("main.extra_index_url")
        if extra_index_url:
            modules_are_installed = install_python_modules(
                modules,
                self.pip_path,
                self.temp_dir,
                "--extra-index-url",
                extra_index_url,
            )
        else:
            modules_are_installed = install_python_modules(modules, self.pip_path, self.temp_dir)

        return modules_are_installed

    @property
    def max_retries(self) -> int:
        return self.manager.config_manager.get("main.max_retries_on_error")

    @property
    def retries_left(self) -> int:
        return max(0, self.max_retries - self._attempts)

    @property
    def python_interpreter_history_file(self) -> Path:
        return get_py_cache()

    def _get_nth_attempt(self) -> int:
        return self._attempts + 1

    def _generate_fixed_code_response(self, original_question: str, code_block: str, error: str) -> str:
        new_question = f"""\
# ORIGINAL QUESTION:
{original_question}

# ANSWER WHICH GENERATED THE ERROR:
{code_block}

# ERROR:
{error}

# TASK:
1. Analyze the error message.
2. Step-by-step, determine how to fix the error.
3. Generate and return **only one single block** in markdown-format of updated Python code that resolves the issue.
4. Do not include any additional code or explanations outside of that one block.
""".strip()
        return self.manager.generate(new_question)

    def _init_python_properties(self, pyenv_path: str, pip_path: str):
        self.pyenv_path = pyenv_path
        self.lib_path = get_lib_path(pyenv_path)
        self.python_executable = get_python_executable(pyenv_path)
        self.pip_path = pip_path

    def _fill_globals_dict(self):
        """
        Fill the globals_dict with the available functions
        These might be available for tool calling or from use in the Python interpreter.
        """
        from owlsight.app.default_functions import OwlDefaultFunctions

        owl_funcs = OwlDefaultFunctions(self.globals_dict)

        # Get all the methods from the OwlDefaultFunctions instance
        default_methods = inspect.getmembers(owl_funcs, predicate=inspect.ismethod)

        # Populate the globals_dict with method names and their corresponding method objects
        for name, method in default_methods:
            self.globals_dict[name] = method

        # add owl_history function to globals_dict
        def owl_history(to_string: bool = False, get_last_response_only: bool = False) -> Union[List[dict], str]:
            """
            Get the chathistory of the current model.

            Parameters
            ----------
            to_string : bool, optional
                If True, returns the history as a formatted string, by default False
            get_last_response_only : bool, optional
                If True, returns only the last response from the history, by default False

            Returns
            -------
            Union[List[dict], str]
                The history as a list of dictionaries or a formatted string.
            """
            processor = self.manager.get_processor()
            if processor:
                history = processor.get_history()
                if get_last_response_only:
                    return history[-1]["content"] if history else ""
                if to_string:
                    return format_chat_history_as_string(history)
                return history
            return "" if to_string else []

        self.globals_dict["owl_history"] = owl_history

        def owl_context_length() -> int:
            """
            Show max context length of the current loaded model.
            Return 0 if no model is loaded or metadata about context length is not available.
            """
            processor = self.manager.get_processor()
            if processor:
                return processor.get_max_context_length()
            return 0

        self.globals_dict["owl_context_length"] = owl_context_length

    def _validate_python_compile_mode(self, python_compile_mode: str) -> None:
        modes = ["exec", "single", "eval"]
        if python_compile_mode not in modes:
            raise ValueError(f"python_compile_mode must be one of {', '.join(modes)}")


def execute_code_with_feedback(
    response: str,
    original_question: str,
    code_executor: CodeExecutor,
    prompt_code_execution: bool = True,
    prompt_retry_on_error: bool = True,
) -> List[Dict]:
    """
    Extract code blocks from a response and execute them with feedback and retry logic.

    Parameters
    ----------
    response : str
        The response containing the code blocks in markdown format.
    original_question : str
        The original question that prompted the code execution.
    code_executor : CodeExecutor
        An instance of CodeExecutor that handles code execution.
    prompt_code_execution : bool
        If True, prompts the user before executing each code block.
        Acts as a safety measure to prevent accidental execution.
    prompt_retry_on_error : bool
        If True, prompts the user before retrying execution after an error.
        Allows the user to edit the code block before retry

    Returns
    -------
    List[Dict]
        A list of dictionaries with execution results, including success status, language, and code.
    """
    results = []

    # Extract code blocks with their associated language
    code_blocks = parse_markdown(response)
    if not code_blocks:
        logger.info("No code blocks found in the response.")
        return results

    execute_all = False
    skip_all = False

    # Iterate over extracted code blocks
    for lang, code_block in code_blocks:
        execute_code = True
        code_is_edited = False
        if prompt_code_execution and not execute_all and not skip_all:
            while True:
                # Use the editable_input function to allow users to edit the code block
                if not code_is_edited:
                    logger.info(f"Code block in {lang.capitalize()}:\n{code_block}")
                    code_block = prompt_code_edit(code_block)
                    code_is_edited = True
                # Provide a menu for the user to choose between "Execute", "Skip", or "Write code to file"
                user_choice = get_user_choice(
                    {
                        "Execute code": None,
                        "Execute all code blocks": None,
                        "Skip code": None,
                        "Skip all code blocks": None,
                        "Write code to file": None,
                    }
                )

                if user_choice == "Execute code":
                    logger.info("Executing code block.")
                    break  # Exit the while loop and execute the code
                elif user_choice == "Execute all code blocks":
                    logger.info("Executing all code blocks.")
                    execute_all = True
                    break
                elif user_choice == "Skip code":
                    logger.info("Skipping code block.")
                    execute_code = False
                    break  # Exit the while loop and skip execution
                elif user_choice == "Skip all code blocks":
                    logger.info("Skipping all code blocks.")
                    skip_all = True
                    execute_code = False
                    break
                elif user_choice == "Write code to file":
                    # Handle writing to a file or going back
                    _handle_write_code_to_file_choice(code_block)
                    # After handling file, stay in the menu for further selection
                    continue  # Stay in the while loop to allow more choices

        if skip_all:
            continue

        if execute_all or execute_code:
            is_success = code_executor.execute_and_retry(lang, code_block, original_question, prompt_retry_on_error)
            result = {"success": is_success, "language": lang, "code": code_block}
            results.append(result)

    return results


def prompt_code_edit(code_block: str) -> str:
    """
    Prompts the user to edit a code block interactively.
    """
    code_block = editable_input(
        "Edit the code block (press ENTER to confirm):\n",
        code_block,
        color=EDIT_CODE_BLOCK_COLOR,
    )
    logger.info(f"Edited Code Block:\n{code_block}")
    return code_block


def _handle_write_code_to_file_choice(code_block: str):
    """
    Handles the process of writing a code block to a file, providing options for entering
    a filename or returning to the main menu.

    Parameters
    ----------
    code_block : str
        The code block to write to the file.
    """
    while True:
        file_choice = get_user_choice(
            {
                "Enter filename": None,
                "Go back": None,
            }
        )

        if file_choice == "Go back":
            logger.info("Returning to the main menu.")
            return  # Return to the main menu

        elif file_choice == "Enter filename":
            file_name = input("Enter the filename: ")
            if file_name:  # If a filename is entered
                try:
                    with open(file_name, "w", encoding="utf-8") as f:
                        f.write(code_block)
                        logger.info(f"Code block written to file: {file_name}")
                    # After writing, return to the main menu without breaking the loop
                    return
                except Exception as e:
                    logger.error(f"Error writing code block to file: {e}. Please try again.")
            else:
                logger.info("No file name entered. Please try again.")


def extract_missing_module(stderr: str) -> Union[str, None]:
    """Extract a missing module from a ModuleNotFoundError exception"""
    match = re.search(r"No module named '(\w+)'", stderr)
    return match.group(1) if match else None
