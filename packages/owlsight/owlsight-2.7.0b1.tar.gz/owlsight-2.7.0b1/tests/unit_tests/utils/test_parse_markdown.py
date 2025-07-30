from owlsight.utils.helper_functions import parse_markdown


def test_parse_markdown():
    # Sample markdown input for Python, Bash, and CMD
    md_string = """
    ```python
    print("Hello, World!")
    ```

    ```bash
    echo "Hello, World!"
    ```

    ```cmd
    dir
    ```
    """

    # Expected output
    expected = [
        ("python", 'print("Hello, World!")'),
        ("bash", 'echo "Hello, World!"'),
        ("cmd", "dir"),
    ]

    result = parse_markdown(md_string)
    assert result == expected, f"Expected {expected}, but got {result}"
