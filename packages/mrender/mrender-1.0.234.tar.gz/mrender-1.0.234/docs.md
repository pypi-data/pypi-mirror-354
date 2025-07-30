# Package: mrender

<details>
<summary>__init__</summary>

<details>
<summary>Contents</summary>

- [def stream](#stream)
</details>

<details>
<summary>def stream</summary>

```python
stream(file_or_content: str)
```

</details>

</details>

<a href='#top'>Back to Top</a>

</details>

<a href='#top'>Back to Top</a>



<details>
<summary>__about__</summary>

</details>

<a href='#top'>Back to Top</a>

</details>

<a href='#top'>Back to Top</a>



<details>
<summary>extract_docs</summary>

  Utilities related to attribute docstring extraction.

<details>
<summary>Contents</summary>

- [class DocstringVisitor](#docstringvisitor)
- [class definitions](#definitions)
- [class itself](#itself)
- [class around](#around)
- [class of](#of)
- [def __init__](#__init__)
- [def visit](#visit)
- [def visit_AnnAssign](#visit_annassign)
- [def visit_Expr](#visit_expr)
- [def _dedent_source_lines](#_dedent_source_lines)
- [def dedent_workaround](#dedent_workaround)
- [def _extract_source_from_frame](#_extract_source_from_frame)
- [def extract_docstrings_from_cls](#extract_docstrings_from_cls)
</details>

<details>
<summary>class DocstringVisitor</summary>

</details>

<details>
<summary>class definitions</summary>

</details>

<details>
<summary>class itself</summary>

</details>

<details>
<summary>class around</summary>

</details>

<details>
<summary>class of</summary>

</details>

<details>
<summary>def __init__</summary>

```python
__init__(self)
```

</details>

<details>
<summary>def visit</summary>

```python
visit(self, node: ast.AST)
```

</details>

<details>
<summary>def visit_AnnAssign</summary>

```python
visit_AnnAssign(self, node: ast.AnnAssign)
```

</details>

<details>
<summary>def visit_Expr</summary>

```python
visit_Expr(self, node: ast.Expr)
```

</details>

<details>
<summary>def _dedent_source_lines</summary>

```python
_dedent_source_lines(source: list[str])
```

</details>

<details>
<summary>def dedent_workaround</summary>

```python
dedent_workaround()
```

</details>

<details>
<summary>def _extract_source_from_frame</summary>

```python
_extract_source_from_frame(cls: type[Any])
```

</details>

<details>
<summary>def extract_docstrings_from_cls</summary>

```python
extract_docstrings_from_cls(cls: type[Any], use_inspect: bool = False)
```

<details>
<summary>Description</summary>

Map model attributes and their corresponding docstring.

    Args:
        cls: The class of the Pydantic model to inspect.
        use_inspect: Whether to skip usage of frames to find the object and use
            the `inspect` module instead.

    Returns:
        A mapping containing attribute names and their corresponding docstring.

</details>

</details>

</details>

<a href='#top'>Back to Top</a>

<details>
<summary>Contents</summary>

- [def extract_docstrings_from_cls](#extract_docstrings_from_cls)
</details>

<details>
<summary>def extract_docstrings_from_cls</summary>

```python
extract_docstrings_from_cls(cls: type[Any], use_inspect: bool = False)
```

<details>
<summary>Function Description</summary>

Map model attributes and their corresponding docstring.

</details>

<details>
<summary>Arguments</summary>

- `cls`: The class of the Pydantic model to inspect.
- `use_inspect`: Whether to skip usage of frames to find the object and use
            the `inspect` module instead.
</details>

<details>
<summary>Returns</summary>

A mapping containing attribute names and their corresponding docstring.
</details>

</details>

</details>

<a href='#top'>Back to Top</a>



<details>
<summary>md</summary>

<details>
<summary>Contents</summary>

- [class Markdown](#markdown)
- [def __init__](#__init__)
- [def generate_markdown](#generate_markdown)
- [def stream](#stream)
- [def recursive_read](#recursive_read)
- [def example](#example)
</details>

<details>
<summary>class Markdown</summary>

<details>
<summary>Description</summary>

Stream formatted JSON-like text to the terminal with live updates.

</details>

</details>

<details>
<summary>def __init__</summary>

```python
__init__(self, data=None, mdargs=None, style="default", save=None)
```

<details>
<summary>Description</summary>

Generate Markdown from JSON with headers based on depth.

</details>

</details>

<details>
<summary>def generate_markdown</summary>

```python
generate_markdown(self, data=None, depth=1)
```

<details>
<summary>Description</summary>

Generate Markdown from JSON with headers based on depth.

</details>

</details>

<details>
<summary>def stream</summary>

```python
stream(self, depth=0)
```

</details>

<details>
<summary>def recursive_read</summary>

```python
recursive_read(file, include=None)
```

</details>

<details>
<summary>def example</summary>

```python
example()
```

</details>

</details>

<a href='#top'>Back to Top</a>

<details>
<summary>Contents</summary>

- [class Markdown](#markdown)
- [def __init__](#__init__)
- [def generate_markdown](#generate_markdown)
</details>

<details>
<summary>class Markdown</summary>

<details>
<summary>Class Description</summary>

Stream formatted JSON-like text to the terminal with live updates.

</details>

  <details>
  <summary>def __init__</summary>

  Generate Markdown from JSON with headers based on depth.

  </details>

  <details>
  <summary>def generate_markdown</summary>

  Generate Markdown from JSON with headers based on depth.

  </details>

</details>

<details>
<summary>def __init__</summary>

```python
__init__(self, data=None, mdargs=None, style="default", save=None)
```

<details>
<summary>Function Description</summary>

Generate Markdown from JSON with headers based on depth.

</details>

</details>

<details>
<summary>def generate_markdown</summary>

```python
generate_markdown(self, data=None, depth=1)
```

<details>
<summary>Function Description</summary>

Generate Markdown from JSON with headers based on depth.

</details>

</details>

</details>

<a href='#top'>Back to Top</a>



<details>
<summary>web2md</summary>

<details>
<summary>Contents</summary>

- [def html_to_markdown_with_depth](#html_to_markdown_with_depth)
- [def traverse_tree](#traverse_tree)
- [def display_markdown_hierarchically](#display_markdown_hierarchically)
- [def cli](#cli)
- [def extract_links](#extract_links)
</details>

<details>
<summary>def html_to_markdown_with_depth</summary>

```python
html_to_markdown_with_depth(html_content, max_depth)
```

</details>

<details>
<summary>def traverse_tree</summary>

```python
traverse_tree(node, current_depth)
```

</details>

<details>
<summary>def display_markdown_hierarchically</summary>

```python
display_markdown_hierarchically(markdown_text, max_depth)
```

</details>

<details>
<summary>def cli</summary>

```python
cli(path, max_depth)
```

</details>

<details>
<summary>def extract_links</summary>

```python
extract_links(markdown_content)
```

<details>
<summary>Description</summary>

Extract links from markdown content.

</details>

</details>

</details>

<a href='#top'>Back to Top</a>

<details>
<summary>Contents</summary>

- [def extract_links](#extract_links)
</details>

<details>
<summary>def extract_links</summary>

```python
extract_links(markdown_content)
```

<details>
<summary>Function Description</summary>

Extract links from markdown content.

</details>

</details>

</details>

<a href='#top'>Back to Top</a>



<details>
<summary>web</summary>

<details>
<summary>Contents</summary>

- [def is_valid_url](#is_valid_url)
- [def expand_and_view_webpage](#expand_and_view_webpage)
- [def display_webpage_content](#display_webpage_content)
- [def prompt_for_webpage](#prompt_for_webpage)
</details>

<details>
<summary>def is_valid_url</summary>

```python
is_valid_url(url)
```

</details>

<details>
<summary>def expand_and_view_webpage</summary>

```python
expand_and_view_webpage(url)
```

</details>

<details>
<summary>def display_webpage_content</summary>

```python
display_webpage_content(url, content)
```

</details>

<details>
<summary>def prompt_for_webpage</summary>

```python
prompt_for_webpage(urls=None)
```

</details>

</details>

<a href='#top'>Back to Top</a>

</details>

<a href='#top'>Back to Top</a>



<details>
<summary>live_pane</summary>

<details>
<summary>Contents</summary>

- [class LivePanelDisplay](#livepaneldisplay)
- [def __init__](#__init__)
- [def update](#update)
- [def __enter__](#__enter__)
- [def __exit__](#__exit__)
</details>

<details>
<summary>class LivePanelDisplay</summary>

</details>

<details>
<summary>def __init__</summary>

```python
__init__(self, msg: str | None = None)
```

</details>

<details>
<summary>def update</summary>

```python
update(self, msg: str, add_sleep: float | None = None)
```

</details>

<details>
<summary>def __enter__</summary>

```python
__enter__(self)
```

</details>

<details>
<summary>def __exit__</summary>

</details>

</details>

<a href='#top'>Back to Top</a>

</details>

<a href='#top'>Back to Top</a>



<details>
<summary>python2json</summary>

<details>
<summary>Contents</summary>

- [def generate_json_spec](#generate_json_spec)
</details>

<details>
<summary>def generate_json_spec</summary>

```python
generate_json_spec(func)
```

</details>

</details>

<a href='#top'>Back to Top</a>

</details>

<a href='#top'>Back to Top</a>



<details>
<summary>render</summary>

<details>
<summary>Contents</summary>

- [class description](#description)
- [def display_class_methods](#display_class_methods)
- [def display_rich_output](#display_rich_output)
- [def create_doc_link](#create_doc_link)
</details>

<details>
<summary>class description</summary>

</details>

<details>
<summary>def display_class_methods</summary>

```python
display_class_methods(cls, markdown=False)
```

</details>

<details>
<summary>def display_rich_output</summary>

```python
display_rich_output(cls)
```

</details>

<details>
<summary>def create_doc_link</summary>

```python
create_doc_link(cls, method_name)
```

</details>

</details>

<a href='#top'>Back to Top</a>

</details>

<a href='#top'>Back to Top</a>



<details>
<summary>docs2md</summary>

<details>
<summary>Contents</summary>

- [def parse_google_docstring](#parse_google_docstring)
- [def generate_feature_list](#generate_feature_list)
- [def generate_examples](#generate_examples)
- [def generate_docs](#generate_docs)
- [def main](#main)
- [def cli](#cli)
</details>

<details>
<summary>def parse_google_docstring</summary>

```python
parse_google_docstring(docstring: str)
```

<details>
<summary>Description</summary>

Parse a Google-style docstring into its components using regex.

</details>

</details>

<details>
<summary>def generate_feature_list</summary>

```python
generate_feature_list(description: str, indent: str = "")
```

<details>
<summary>Description</summary>

Generate a markdown list of features from the description.

</details>

</details>

<details>
<summary>def generate_examples</summary>

```python
generate_examples(examples: List[str], indent: str = "")
```

<details>
<summary>Description</summary>

Generate a markdown code block with examples.

</details>

</details>

<details>
<summary>def generate_docs</summary>

```python
generate_docs(file_path: str, is_package: bool = False, indent: str = "")
```

<details>
<summary>Description</summary>

Generate markdown documentation for a given Python file.

</details>

</details>

<details>
<summary>def main</summary>

```python
main(path: str, output_file: str)
```

<details>
<summary>Description</summary>

Generate markdown documentation for all Python files in a given path.

</details>

</details>

<details>
<summary>def cli</summary>

```python
cli(path: str, output_file: str)
```

<details>
<summary>Description</summary>

Command-line interface for generating markdown documentation.

    Args:
        path (str): The path to the Python file or directory.
        output_file (str): The output file to save the generated markdown.

</details>

</details>

</details>

<a href='#top'>Back to Top</a>

<details>
<summary>Contents</summary>

- [def parse_google_docstring](#parse_google_docstring)
- [def generate_feature_list](#generate_feature_list)
- [def generate_examples](#generate_examples)
- [def generate_docs](#generate_docs)
- [def main](#main)
- [def cli](#cli)
</details>

<details>
<summary>def parse_google_docstring</summary>

```python
parse_google_docstring(docstring: str)
```

<details>
<summary>Function Description</summary>

Parse a Google-style docstring into its components using regex.

</details>

</details>

<details>
<summary>def generate_feature_list</summary>

```python
generate_feature_list(description: str, indent: str = "")
```

<details>
<summary>Function Description</summary>

Generate a markdown list of features from the description.

</details>

</details>

<details>
<summary>def generate_examples</summary>

```python
generate_examples(examples: List[str], indent: str = "")
```

<details>
<summary>Function Description</summary>

Generate a markdown code block with examples.

</details>

</details>

<details>
<summary>def generate_docs</summary>

```python
generate_docs(file_path: str, is_package: bool = False, indent: str = "")
```

<details>
<summary>Function Description</summary>

Generate markdown documentation for a given Python file.

</details>

</details>

<details>
<summary>def main</summary>

```python
main(path: str, output_file: str)
```

<details>
<summary>Function Description</summary>

Generate markdown documentation for all Python files in a given path.

</details>

</details>

<details>
<summary>def cli</summary>

```python
cli(path: str, output_file: str)
```

<details>
<summary>Function Description</summary>

Command-line interface for generating markdown documentation.

</details>

</details>

</details>

<a href='#top'>Back to Top</a>



<details>
<summary>panel</summary>

<details>
<summary>Contents</summary>

- [class LivePanelDisplay](#livepaneldisplay)
- [def __init__](#__init__)
- [def update](#update)
- [def __enter__](#__enter__)
- [def __exit__](#__exit__)
</details>

<details>
<summary>class LivePanelDisplay</summary>

</details>

<details>
<summary>def __init__</summary>

```python
__init__(self, msg: str | None = None)
```

</details>

<details>
<summary>def update</summary>

```python
update(self, msg: str, add_sleep: float | None = None)
```

</details>

<details>
<summary>def __enter__</summary>

```python
__enter__(self)
```

</details>

<details>
<summary>def __exit__</summary>

</details>

</details>

<a href='#top'>Back to Top</a>

</details>

<a href='#top'>Back to Top</a>



<details>
<summary>main</summary>

<details>
<summary>Contents</summary>

- [def generate_summary](#generate_summary)
- [def cli](#cli)
</details>

<details>
<summary>def generate_summary</summary>

```python
generate_summary(markdown_content)
```

</details>

<details>
<summary>def cli</summary>

```python
cli(input: str = None, output: str = None, format: str = "md", depth: int = 3, docs: bool = False, web: bool = False)
```

<details>
<summary>Description</summary>

Process input file, directory, or web URL and generate output.

    If no input is provided, this help message will be displayed.
    If --web is specified or the input starts with http:// or https://, the input is treated as a web URL.

</details>

</details>

</details>

<a href='#top'>Back to Top</a>

<details>
<summary>Contents</summary>

- [def cli](#cli)
</details>

<details>
<summary>def cli</summary>

```python
cli(input: str = None, output: str = None, format: str = "md", depth: int = 3, docs: bool = False, web: bool = False)
```

<details>
<summary>Function Description</summary>

Process input file, directory, or web URL and generate output.

    If no input is provided, this help message will be displayed.
    If --web is specified or the input starts with http:// or https://, the input is treated as a web URL.

</details>

</details>

</details>

<a href='#top'>Back to Top</a>



