import pytest
from mrender import md, web, web2md
from rich.markdown import Markdown as RichMarkdown
import pytest
from click.testing import CliRunner
from mrender.main import cli
from mrender.docs2md import generate_docs
import sys
import os


def test_markdown_class():
    markdown = md.Markdown(data="# Test Markdown")
    assert isinstance(markdown, md.Markdown)
    assert markdown.lines == ["# Test Markdown"]

def test_markdown_class_no_data():
    markdown = md.Markdown()
    assert isinstance(markdown, md.Markdown)
    assert markdown.lines == []

def test_markdown_stream(capsys):
    markdown = md.Markdown(data={"key": "value"})
    markdown.stream()
    captured = capsys.readouterr()
    assert "key" in captured.out
    assert "value" in captured.out

def test_recursive_read(tmp_path):
    test_file = tmp_path / "test.json"
    test_file.write_text('{"test": "content"}')
    result = md.recursive_read(str(test_file))
    assert str(test_file) in result
    assert result[str(test_file)] == '{"test": "content"}'

def test_is_valid_url():
    assert web.is_valid_url("https://www.example.com")
    assert not web.is_valid_url("not_a_url")

def test_cli_web_content(mocker):
    mock_get = mocker.patch('requests.get')
    mock_html_to_markdown = mocker.patch('mrender.main.html_to_markdown_with_depth')
    mock_display_markdown = mocker.patch('mrender.main.display_markdown_hierarchically')

    mock_response = mocker.Mock()
    mock_response.text = "<html><body>Sample content</body></html>"
    mock_get.return_value = mock_response

    mock_html_to_markdown.return_value = "# Sample Markdown"

    runner = CliRunner()
    result = runner.invoke(cli, ["https://www.example.com"])

    assert result.exit_code == 0
    mock_get.assert_called_once_with("https://www.example.com")
    mock_html_to_markdown.assert_called_once_with("<html><body>Sample content</body></html>", 3)
    mock_display_markdown.assert_called_once_with("# Sample Markdown", 3)

def test_html_to_markdown_with_depth():
    html_content = "<html><body><h1>Test</h1><p>This is a test.</p></body></html>"
    result = web2md.html_to_markdown_with_depth(html_content, max_depth=2)
    assert "# Test" in result
    assert "This is a test." in result

def test_display_markdown_hierarchically(capsys):
    markdown_text = "# Header\n## Subheader\nContent"
    web2md.display_markdown_hierarchically(markdown_text, max_depth=2)
    captured = capsys.readouterr()
    assert "Header" in captured.out
    assert "Subheader" in captured.out
    assert "Content" in captured.out


@pytest.fixture
def runner():
    return CliRunner()

def test_cli_docs_no_docstring(runner, tmp_path):
    # Create a temporary Python file without a docstring
    test_file = tmp_path / "test_module.py"
    test_file.write_text("def test_function():\n    pass\n")

    result = runner.invoke(cli, [str(test_file), "--docs"])
    assert result.exit_code == 0
    assert "Module: test_module" in result.output
    assert "No module description available." in result.output

def test_generate_docs(tmp_path):
    # Create a temporary Python file
    test_file = tmp_path / "test_module.py"
    test_file.write_text("""
        \"\"\"This is a test module.\"\"\"

        def test_function():
            \"\"\"This is a test function.\"\"\"
            pass
    """)

    # Generate docs
    docs = generate_docs(str(test_file))

    # Assert the generated docs contain the module description
    assert "This is a test module." in docs
    # Assert the generated docs contain the function description
    assert "This is a test function." in docs

def test_cli_docs_with_docstring(runner, tmp_path):
    # Create a temporary Python file with a docstring
    test_file = tmp_path / "test_module_with_doc.py"
    test_file.write_text('"""This is a test module."""\n\ndef test_function():\n    pass\n')

    result = runner.invoke(cli, [str(test_file), "--docs"])
    assert result.exit_code == 0
    assert "Module: test_module_with_doc" in result.output
    assert "This is a test module." in result.output

def test_cli_docs_with_directory(runner, tmp_path):
    # Create a temporary directory with multiple Python files
    test_dir = tmp_path / "test_module_dir"
    test_dir.mkdir()
    (test_dir / "file1.py").write_text('"""File 1 docstring."""\ndef func1():\n    pass\n')
    (test_dir / "file2.py").write_text('"""File 2 docstring."""\ndef func2():\n    pass\n')

    result = runner.invoke(cli, [str(test_dir), "--docs"])
    assert result.exit_code == 0
    assert "Module: file1" in result.output
    assert "File 1 docstring." in result.output
    assert "Module: file2" in result.output
    assert "File 2 docstring." in result.output


def test_cli_docs_with_package(runner, tmp_path):
    # Create a temporary package directory
    package_dir = tmp_path / "mrender"
    package_dir.mkdir()
    (package_dir / "__init__.py").write_text('"""Package docstring."""\n')
    (package_dir / "module1.py").write_text('"""Module 1 docstring."""\ndef func1():\n    pass\n')
    (package_dir / "module2.py").write_text('"""Module 2 docstring."""\ndef func2():\n    pass\n')

    result = runner.invoke(cli, [str(package_dir), "--docs"])
    assert result.exit_code == 0
    print(f"Test output: {result.output}")  # Add this line for debugging
    assert "# Package: mrender" in result.output
    assert "Package docstring." in result.output
    assert "# Module: module1" in result.output
    assert "Module 1 docstring." in result.output
    assert "# Module: module2" in result.output
    assert "Module 2 docstring." in result.output

def test_cli_no_input(runner):
    result = runner.invoke(cli, [])
    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "Process input file, directory, or web URL and generate output." in result.output

def test_cli_help_option(runner):
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "Process input file, directory, or web URL and generate output." in result.output
    assert "--web" in result.output
    assert "Process input as a web URL" in result.output
