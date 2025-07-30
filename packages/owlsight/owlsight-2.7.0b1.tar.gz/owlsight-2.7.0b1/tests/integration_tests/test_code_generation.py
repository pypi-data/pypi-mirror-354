import pytest
import sys
import tempfile
import os

sys.path.append("src")
sys.path.append("tests")
from owlsight.utils.code_execution import CodeExecutor, execute_code_with_feedback
from owlsight.utils.venv_manager import get_pyenv_path, get_pip_path


@pytest.fixture
def code_executor(text_generation_manager):
    return CodeExecutor(
        text_generation_manager,
        temp_dir="temp_dir",
        pip_path="pip",
        pyenv_path="venv",
    )


def test_code_executor_execute_python_code_succesfully(code_executor: CodeExecutor):
    result = code_executor.execute_and_retry("python", "print('Hello')", "original question")
    assert result


def test_code_executor_python_state_is_saved(code_executor: CodeExecutor):
    # Test that variables are correctly set in the state after execution
    code_executor.execute_python_code("x = 10")
    assert code_executor.globals_dict.get("x") == 10

    # Test executing another block of code that uses the state
    code_executor.execute_python_code("y = x + 5")
    assert code_executor.globals_dict.get("y") == 15

    # Test that the state is persistent across executions
    assert code_executor.globals_dict.get("x") == 10  # x should still be available


def test_clear_state(code_executor: CodeExecutor):
    # Set some state
    code_executor.execute_python_code("x = 20")
    assert code_executor.globals_dict.get("x") == 20

    # Clear the state and check if it's removed
    code_executor.globals_dict.clear()
    assert code_executor.globals_dict.get("x") is None  # State should be cleared


def test_code_executor_install_missing_module_in_venv(text_generation_manager):
    # arrange
    module_name = "tinydb"
    question = f"Use python to generate code which uses the '{module_name}' module"
    model_response = f"""
    Sure! Here is a Python code snippet that imports the '{module_name}' module:
    ```python
    import {module_name} as md\na = 5
    ```
    """.strip()
    with tempfile.TemporaryDirectory() as temp_dir:
        pyenv_path = get_pyenv_path()
        pip_path = get_pip_path(pyenv_path)

        code_executor = CodeExecutor(text_generation_manager, pyenv_path, pip_path, temp_dir)
        results = execute_code_with_feedback(
            model_response,
            question,
            code_executor,
            prompt_code_execution=False,
        )

        assert isinstance(results, list)
        assert len(results) == 1
        assert isinstance(results[0], dict)
        assert results[0]["success"]

        # lib is installed in venv
        assert module_name in os.listdir(code_executor.temp_dir)

        # state is saved correctly
        assert code_executor.globals_dict.get("a") == 5
