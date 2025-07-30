from typing import List, Tuple, Dict, Any, Union
import ast
import os
import shutil
import re
import traceback
import inspect
from datetime import datetime, timedelta
import json
from pathlib import Path
from functools import wraps

from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style

from owlsight.utils.custom_classes import MediaObject, DoubleBracketsTag, _AVAILBLE_DB_TAGS
from owlsight.utils.logger import logger


def safe_lru_cache(maxsize=128, typed=False):
    """
    A safer version of lru_cache that only caches successful function calls.
    
    This decorator wraps Python's standard lru_cache but adds error handling.
    When the decorated function raises an exception, the call is not cached,
    and the function is executed directly on subsequent calls with the same arguments.
    This is particularly useful for functions that might fail with unhashable 
    arguments (like lists) or network operations that may occasionally fail.
    
    Parameters
    ----------
    maxsize : int, optional
        Maximum size of the cache, by default 128
    typed : bool, optional
        If True, arguments of different types will be cached separately, by default False
        
    Returns
    -------
    Callable
        Decorated function with safe LRU caching behavior
        
    Examples
    --------
    >>> @safe_lru_cache(maxsize=100)
    ... def fetch_data(url_list):
    ...     # Even if url_list is unhashable (like a list), this won't fail
    ...     return [fetch(url) for url in url_list]
    """
    def decorator(func):
        # Use a dictionary for our cache
        cache = {}
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create a cache key that works with unhashable types
            # Convert lists to tuples and use repr for other unhashable types
            def make_key(args, kwargs):
                key_parts = []
                for arg in args:
                    if isinstance(arg, list):
                        processed = tuple(arg)
                    else:
                        try:
                            hash(arg)
                            processed = arg
                        except TypeError:
                            processed = repr(arg)
                    if typed:
                        key_parts.append((processed, type(arg)))
                    else:
                        key_parts.append(processed)

                for k, v in sorted(kwargs.items()):
                    if isinstance(v, list):
                        processed = tuple(v)
                    else:
                        try:
                            hash(v)
                            processed = v
                        except TypeError:
                            processed = repr(v)
                    if typed:
                        key_parts.append((k, processed, type(v)))
                    else:
                        key_parts.append((k, processed))

                return tuple(key_parts)
            
            key = make_key(args, kwargs)
            
            # Check if result is in cache
            if key in cache:
                return cache[key]
            
            # Not in cache, call the function
            try:
                result = func(*args, **kwargs)
                # Cache successful result
                cache[key] = result
                
                # Implement LRU behavior - remove oldest entries if cache exceeds maxsize
                if maxsize > 0 and len(cache) > maxsize:
                    # Simple approach: remove oldest entry
                    # (In a real implementation, you'd track access time for true LRU)
                    cache.pop(next(iter(cache)))
                
                return result
            except Exception as e:
                # If an exception occurs, don't cache the result
                # Just re-raise the exception
                raise
                
        return wrapper
    
    return decorator

def parse_xml(string: str, tag: str) -> str:
    """
    Parse XML-like tags from text into a string.

    Parameters
    ----------
    string : str
        The text containing XML-like tags to parse.
    tag : str
        The tag name to extract.

    Returns
    -------
    str
        The content of the specified tag, or an empty string if not found.

    Example
    -------
    >>> text = '<goal>My goal</goal><step>Step 1</step>'
    >>> parse_xml(text, 'goal')
    'My goal'
    >>> parse_xml(text, 'step')
    'Step 1'
    >>> parse_xml(text, 'missing')
    ''
    """
    match = re.search(rf"<{tag}>(.*?)</{tag}>", string, re.DOTALL)
    return match.group(1) if match else ""


def parse_markdown(md_string: str) -> List[Tuple[str, str]]:
    """
    Parses language and code blocks from a markdown string.

    Returns
    -------
    list of tuples: Each tuple contains (language, code)
    """
    pattern = r"```(\w+)([\s\S]*?)```"
    return [(match[0].strip(), match[1].strip()) for match in re.findall(pattern, md_string)]


def parse_python_placeholders(text: str, var_dict: Dict[str, Any]) -> Any:
    """
    Evaluates expressions inside {{...}} in the given text and replaces them with the result.
    Correctly handles expressions containing braces or other special characters.

    Parameters
    ----------
    text : str
        The input string containing placeholders in the form of `{{...}}`.
    var_dict : dict
        A dictionary where keys correspond to variables used in placeholders.

    Returns
    -------
    Any
        The evaluated object if the entire string is a single placeholder,
        otherwise the string with placeholders replaced.
    """

    def evaluate_expression(expr: str) -> Any:
        try:
            safe_globals = {
                "__builtins__": {
                    "abs": abs,
                    "all": all,
                    "any": any,
                    "bin": bin,
                    "bool": bool,
                    "chr": chr,
                    "divmod": divmod,
                    "enumerate": enumerate,
                    "filter": filter,
                    "float": float,
                    "format": format,
                    "hash": hash,
                    "hex": hex,
                    "int": int,
                    "isinstance": isinstance,
                    "issubclass": issubclass,
                    "iter": iter,
                    "len": len,
                    "list": list,
                    "map": map,
                    "max": max,
                    "min": min,
                    "next": next,
                    "oct": oct,
                    "ord": ord,
                    "pow": pow,
                    "range": range,
                    "repr": repr,
                    "reversed": reversed,
                    "round": round,
                    "sorted": sorted,
                    "str": str,
                    "sum": sum,
                    "tuple": tuple,
                    "zip": zip,
                    "dict": dict,
                    "set": set,
                    "frozenset": frozenset,
                    "datetime": datetime,
                    "timedelta": timedelta,
                }
            }
            safe_globals.update(var_dict)
            return eval(expr, safe_globals, {})
        except Exception as e:
            error_message = f"Error evaluating '{expr}': {str(e)}"
            raise type(e)(error_message) from None

    # Pattern to match balanced double braces
    pattern = r"""
        \{\{            # Opening double braces {{
        (?P<expr>       # Start of named group 'expr'
            [^\{\}]*    # Match any characters except { or }
            (?:         # Non-capturing group
                \{[^\{\}]*\} # Match balanced braces
                [^\{\}]*    # Match any characters except { or }
            )*          # Zero or more times
        )               # End of named group 'expr'
        \}\}            # Closing double braces }}
    """
    regex = re.compile(pattern, re.VERBOSE)

    # Function to replace each placeholder
    def replace_match(m):
        expr = m.group("expr")
        evaluated = evaluate_expression(expr.strip())
        return str(evaluated)

    # Check if the entire text is a single placeholder
    if regex.fullmatch(text):
        expr = regex.fullmatch(text).group("expr")
        return evaluate_expression(expr.strip())
    else:
        return regex.sub(replace_match, text)


def editable_input(prompt_text: str, default_value: str, color: str = "ansicyan") -> str:
    """
    Displays a prompt with a pre-filled editable string and custom color for the default value.

    Parameters
    ----------
    prompt_text : str
        The prompt message shown before the editable string.
    default_value : str
        The string that will be pre-filled and editable by the user.
    color : str, optional
        The color to apply to the default value in the prompt message, default is 'ansicyan'.

    Examples
    --------
    >>> editable_input("Enter your name: ", "John")
    Enter your name: "John" -> Enter your name: "Johnny"
    'Johnny'

    Returns
    -------
    str
        The string edited by the user.
    """
    style = Style.from_dict({"prompt_text": color})

    # Prepare the prompt text with custom color using HTML
    formatted_prompt = HTML(f"<ansicyan>{prompt_text}</ansicyan>")

    # Get the result from the prompt (default value is shown but not styled)
    result = prompt(formatted_prompt, default=default_value, style=style)

    return result.strip()


def force_delete(directory: Union[str, Path]) -> None:
    """
    Forcefully deletes a directory if it exists.

    Parameters
    ----------
    directory : Union[str, Path]
        Path to the directory to delete
    """
    directory = Path(directory)
    if directory.exists():
        try:
            shutil.rmtree(directory)
        except Exception:
            logger.error(f"Error deleting directory {directory}:\n{traceback.format_exc()}")


def remove_temp_directories(lib_path: Union[str, Path]) -> None:
    """
    Removes lingering temporary directories in the virtual environment's library path.

    Parameters
    ----------
    lib_path : Union[str, Path]
        Path to the library directory to clean
    """
    lib_path = Path(lib_path)
    if not lib_path.exists():
        logger.warning(f"Library path does not exist: {lib_path}")
        return

    for d in lib_path.iterdir():
        if d.name.startswith("tmp"):
            logger.info(f"Removing temporary directory: {d}")
            force_delete(d)


def format_error_message(e: Exception) -> str:
    """
    Format an error message to be displayed to the user.

    Parameters
    ----------
    error : Exception
        The exception that occurred.

    Returns
    -------
    str
        The formatted error message.
    """
    return "{e.__class__.__name__}: {e}".format(e=e)


def convert_to_real_type(value):
    """
    Convert a string to its real type if possible (e.g., 'True' -> True, '3.14' -> 3.14).
    """
    if not isinstance(value, str):
        return value

    # Try to evaluate the string and return the result only if it's not a string
    try:
        evaluated_value = ast.literal_eval(value)
        # Only return the evaluated value if it is not a string
        if not isinstance(evaluated_value, str):
            return evaluated_value
    except (ValueError, SyntaxError):
        pass  # Return original string if evaluation fails

    return value  # Return the original string if it's not evaluable


def os_is_windows():
    return os.name == "nt"


def validate_input_params(func: callable, kwargs: dict):
    """
    Validate the keyword arguments passed to a class against the __init__ signature.

    Parameters
    ----------
    func : callable
        The callable of which arguments are being validated.
    kwargs : dict
        A dictionary of keyword arguments to validate.

    Raises
    ------
    ValueError
        If there are invalid parameters.
    """
    # Extract the parameters from the __init__ method of the class
    sig = inspect.signature(func)
    sig_params = sig.parameters

    valid_params = [param_name for param_name in sig_params if param_name != "self"]

    # Check for any extra parameters in kwargs that are not in the __init__ signature
    for key in kwargs:
        if key not in sig_params:
            raise ValueError(
                f"Invalid argument: '{key}' is not a valid parameter for '{func.__name__}'\nValid parameters: {valid_params}"
            )


def flatten_dict(d, parent_key="", sep=".") -> dict:
    """Flatten a nested dictionary."""
    flattened = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            flattened.update(flatten_dict(v, new_key, sep=sep))
        else:
            flattened[new_key] = v
    return flattened


def parse_media_tags(text: str, var_dict: Dict[str, Any]) -> Tuple[str, Dict[str, MediaObject]]:
    """
    Parse media syntax patterns [[tag:path|option1=value1|...]] in text and evaluate any
    Python expressions inside {{...}}. Returns the modified text and a dictionary of
    media objects with their options.

    Parameters
    ----------
    text : str
        The input string containing media placeholders and optional Python expressions
    var_dict : dict
        A dictionary where keys correspond to variables used in Python expressions

    Returns
    -------
    Tuple[str, MediaObjects]
        A tuple containing:
        - The text with media placeholders replaced with unique identifiers
        - A dictionary mapping identifiers to MediaObject instances

    Examples
    --------
    >>> var_dict = {"folder": "images", "filename": "cat.jpg"}
    >>> text = "Analyze this: [[image:{{folder}}/{{filename}}|width=512]]"
    >>> result, media_objects = parse_media_tags(text, var_dict)
    >>> print(result)
    'Analyze this: __MEDIA_0__'
    >>> print(media_objects)
    {
        '__MEDIA_0__': MediaObject(
            tag='image',
            path='images/cat.jpg',
            options={'width': '512'}
        )
    }
    """

    def validate_media_syntax(text: str) -> None:
        # Check for valid media tags
        invalid_tags = re.findall(r"\[\[(\w+):", text)
        valid_tags = _AVAILBLE_DB_TAGS
        for t in invalid_tags:
            if t not in valid_tags:
                raise ValueError(f"Invalid media tag: {t}. Must be one of {valid_tags}")

        # Check for missing paths
        if re.search(r"\[\[\w+:\s*(\||\]\])", text):
            raise ValueError("Media path cannot be empty")

        # Check for invalid option format
        option_pattern = r"\|\|(?!\w+=)[^]|]*(?=[\]|])"
        invalid_options = re.findall(option_pattern, text)
        if invalid_options:
            raise ValueError(f"Invalid option format: {invalid_options[0].strip()}. Must be key=value")

    validate_media_syntax(text)

    pattern = r"""\[\[
        (?P<tag>image|audio|video):  # Media tag
        (?P<path>[^\|\]]+)            # Path (anything until || or ])
        (?:\|\|(?P<options>[^\]]+))?    # Optional options after ||
        \]\]"""

    media_objects: Dict[str, MediaObject] = {}
    replacement_count = 0

    def replace_match(match) -> str:
        nonlocal replacement_count

        media_tag: DoubleBracketsTag = match.group("tag")  # type: ignore
        raw_path = match.group("path")
        options_str = match.group("options") or ""

        # Process the path first - evaluate any Python expressions
        processed_path = parse_python_placeholders(raw_path, var_dict)

        # Process options
        options: Dict[str, str] = {}
        if options_str:
            for option in options_str.split("||"):
                if "=" in option:
                    key, value = option.split("=", 1)
                    # Evaluate Python expressions in option values and convert to string
                    processed_value = str(parse_python_placeholders(value.strip(), var_dict))
                    options[key.strip()] = processed_value

        # Create unique identifier
        identifier = f"__MEDIA_{replacement_count}__"
        replacement_count += 1

        # Store media object information using the MediaObject class
        media_objects[identifier] = MediaObject(tag=media_tag, path=processed_path, options=options)

        return identifier

    # Use verbose flag for multiline regex pattern
    regex = re.compile(pattern, re.VERBOSE)

    # First replace media placeholders
    processed_text = regex.sub(replace_match, text)

    # Then evaluate any remaining Python expressions in the text
    processed_text = parse_python_placeholders(processed_text, var_dict)

    return processed_text, media_objects


def extract_square_bracket_tags(
    text: str, tag: Union[str, List[str]], key: str = "path"
) -> List[Union[str, Dict[str, str]]]:
    """
    Extracts square bracket tags from a string and returns a list of either strings or dictionaries.

    Parameters
    ----------
    text : str
        The input string containing square bracket tags.

    tag : Union[str, List[str]]
        A tag or list of tags to search for. Each tag must be one of _AVAILBLE_DB_TAGS.

    key : str, optional
        The key to use for the tag value, by default "path".

    Returns
    -------
    List[Union[str, Dict[str, str]]]
        A list of strings (input text) and/or dictionaries (tag).
    """
    # Convert single tag to list if necessary
    tags = [tag] if isinstance(tag, str) else tag

    if not all(t in _AVAILBLE_DB_TAGS for t in tags):
        raise ValueError(f"Invalid tag in {tags}. Must be a subset of {_AVAILBLE_DB_TAGS}")

    # Construct regex pattern to capture any of the provided tags
    pattern = r"\[\[(?P<tag>" + "|".join(re.escape(t) for t in tags) + "):" + r"(?P<value>.*?)\]\]"
    matches = list(re.finditer(pattern, text))
    result = []
    prev_end = 0

    for match in matches:
        start, end = match.start(), match.end()
        if start > prev_end:
            part = text[prev_end:start].strip()
            if part:
                result.append(part)
        d = {"tag": match.group("tag"), key: match.group("value")}
        result.append(d)
        prev_end = end

    if prev_end < len(text):
        part = text[prev_end:].strip()
        if part:
            result.append(part)

    return result


def parse_xml_tags_to_dict(text: str) -> dict:
    """
    Parse XML-like tags from text into a dictionary.

    Parameters
    ----------
    text : str
        The text containing XML-like tags to parse

    Returns
    -------
    dict
        Dictionary with tag names as keys and their content as values

    Example
    -------
    >>> text = '<goal>My goal</goal><step>Step 1</step>'
    >>> parse_xml_tags(text)
    {'goal': 'My goal', 'step': 'Step 1'}
    """
    # Strip any leading/trailing whitespace
    text = text.strip()

    # Dictionary to store results
    result = {}

    # Find all tags and their content
    pattern = r"<(\w+)>(.*?)</\1>"
    matches = re.findall(pattern, text, re.DOTALL)

    # Store each tag's content in the dictionary
    # Strip whitespace and newlines from the beginning and end of content
    for tag, content in matches:
        result[tag] = content.strip()

    return result


def parse_function_call(input_str: str) -> tuple[Union[str, None], Union[dict, None]]:
    """
    Parses a string for a JSON-like function call pattern of the form:
    {"name": "function_name", "arguments": { ... }}

    Returns:
        tuple: (function_name, arguments_dict) if parsing succeeds,
               (None, None) if parsing fails
    """
    pattern = r'\{"name":\s*"([^"]+)"[^}]*?:\s*(\{[^}]+\})'
    match = re.search(pattern, input_str)
    if not match:
        return None, None

    func_name = match.group(1)
    args_str = match.group(2)
    try:
        arguments = json.loads(args_str)
        return func_name, arguments
    except json.JSONDecodeError:
        return None, None


def function_call_to_python_code(func_name: str, arguments: dict) -> str:
    """
    Transforms a function name and arguments dict into a Python code string in markdown format.
    """

    def parse_value(value: str):
        """Safely convert string representations to proper Python types"""
        try:
            # Handle numeric types
            if value.isdigit():
                return int(value)
            if value.replace(".", "", 1).isdigit():
                return float(value)
            # Handle boolean values
            if value.lower() in ("true", "false"):
                return value.lower() == "true"
            # Handle quoted strings
            if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                return value[1:-1]
            # Handle lists/dicts
            if value.startswith(("[", "{")):
                return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            pass
        return value  # Return as string literal if all else fails

    processed_args = []
    for key, value in arguments.items():
        parsed = parse_value(str(value))
        if isinstance(parsed, str):
            # Add quotes if not already present
            if not (parsed.startswith(('"', "'")) and parsed.endswith(('"', "'"))):
                parsed = f"'{parsed}'"
        processed_args.append(f"{key}={parsed}")

    code_line = f"final_result = {func_name}({', '.join(processed_args)})"
    return f"```python\n{code_line}\n```"


def parse_function_call_to_python_code(input_str: str) -> str:
    """
    Parses a string for a JSON-like function call pattern and transforms it into
    a Python markdown code block. If parsing fails, returns the original string.
    """
    try:
        # Parse input with JSON loader to handle whitespace and types
        data = json.loads(input_str)
        name = data.get("name", "")
        arguments = data.get("arguments", {})

        # Convert arguments with proper type handling
        args = []
        for key, value in arguments.items():
            if isinstance(value, bool):
                args.append(f"{key}={str(value)}")
            elif value is None:
                args.append(f"{key}=None")
            elif isinstance(value, str):
                args.append(f"{key}={repr(value)}")
            else:
                args.append(f"{key}={value}")

        code_line = f"final_result = {name}({', '.join(args)})"
        return f"```python\n{code_line}\n```"
    except json.JSONDecodeError:
        return input_str


def format_chat_history_as_string(history: List[dict]) -> str:
    """
    Formats a chathistory as a string with clear visual separation between messages.

    Parameters
    ----------
    history : List[dict]
        The chathistory to format.

    Returns
    -------
    str
        The formatted chathistory with enhanced visual separation.
    """
    formatted = []
    message_separator = "\n" + "=" * 80 + "\n"  # Longer, more distinct separator

    for item in history:
        # Add message header with role in uppercase
        formatted.append(f"【 {item['role'].upper()} 】")

        # Add content with indentation for better readability
        content_lines = item["content"].split("\n")
        indented_content = "\n    ".join(content_lines)  # Four spaces indentation
        formatted.append(f"Content:\n    {indented_content}")

        # Add separator after each message
        formatted.append(message_separator)

    return "".join(formatted)
