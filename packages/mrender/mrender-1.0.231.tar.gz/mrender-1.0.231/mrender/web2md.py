import re
from pathlib import Path

import requests

from mrender.md import Markdown
from lxml.etree import Element

def html_to_markdown_with_depth(element: Element, depth: int = 0) -> str:
    """Recursively convert HTML element and its children to Markdown."""
    markdown_lines = []
    indent = ' ' * depth
    
    if element.name is not None:
        # Handle headers
        if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = int(element.name[1])  # Get header level
            markdown_lines.append(f"{indent}{'#' * level} {element.get_text(strip=True)}")
        
        # Handle paragraphs
        elif element.name == 'p':
            markdown_lines.append(f"{indent}{element.get_text(strip=True)}")
        
        # Handle unordered lists
        elif element.name == 'ul':
            for li in element.find_all('li', recursive=False):
                markdown_lines.append(f"{indent}- {html_to_markdown_with_depth(li, depth + 2)}")

        # Handle ordered lists
        elif element.name == 'ol':
            for i, li in enumerate(element.find_all('li', recursive=False), start=1):
                markdown_lines.append(f"{indent}{i}. {html_to_markdown_with_depth(li, depth + 2)}")

        # Handle other tags (e.g., blockquotes, code blocks)
        elif element.name == 'blockquote':
            markdown_lines.append(f"{indent}> {element.get_text(strip=True)}")

        elif element.name == 'code':
            markdown_lines.append(f"{indent}```\n{element.get_text(strip=True)}\n```")

        # Handle other nested tags recursively
        else:
            for child in element.children:
                markdown_lines.extend(html_to_markdown_with_depth(child, depth))

    # If element has no tag name, treat it as text
    else:
        markdown_lines.append(f"{indent}{element}")

    return ''.join(markdown_lines)

def display_markdown_hierarchically(markdown_text, max_depth):
    md = Markdown(markdown_text)
    md.stream(max_depth)


def cli(path, max_depth):
    if Path(path).exists():
        html = Path(path).read_text()
    elif requests.get(path).status_code == 200:
        html = requests.get(path, timeout=10).text

    markdown_output = html_to_markdown_with_depth(html, max_depth)



    display_markdown_hierarchically(markdown_output, max_depth)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python web2md.py <path> <max_depth>")
        sys.exit(1)
    
    cli(sys.argv[1], int(sys.argv[2]))
    # # Sample HTML content
    # html_content = """
    # <html>
    #     <head><title>Sample Page</title></head>
    #     <body>
    #         <h1>Heading 1</h1>
    #         <p>This is a <strong>sample</strong> paragraph with <a href="https://example.com">a link</a>.</p>
    #         <div>
    #             <h2>Subheading</h2>
    #             <ul>
    #                 <li>First item</li>
    #                 <li>Second item</li>
    #             </ul>
    #         </div>
    #         <footer>
    #             <p>Footer content</p>
    #         </footer>
    #     </body>
    # </html>
    # """

    # max_depth = 3
    # markdown_output = html_to_markdown_with_depth(html_content, max_depth)

    # print("Markdown Output:")
    # print(markdown_output)

    # display_markdown_hierarchically(markdown_output, max_depth)import re

def extract_links(markdown_content):
    """Extract links from markdown content."""
    link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
    links = re.findall(link_pattern, markdown_content)
    return [{"text": text, "url": url} for text, url in links]
