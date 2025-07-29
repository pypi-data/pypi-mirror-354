from _typeshed import Incomplete
from mrender.docs2md import generate_docs as generate_docs
from mrender.md import Markdown as Markdown, recursive_read as recursive_read
from mrender.web2md import display_markdown_hierarchically as display_markdown_hierarchically, extract_links as extract_links, html_to_markdown_with_depth as html_to_markdown_with_depth
from requests.exceptions import RequestException as RequestException

console: Incomplete

def generate_summary(markdown_content: str): ...
def cli(input: str = None, output: str = None, format: str = 'md', depth: int = 3, docs: bool = False, web: bool = False) -> None: ...
