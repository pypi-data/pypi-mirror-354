import importlib.util
import logging as log
import os
import re
import sys
from pathlib import Path

import requests
import rich_click as click
from requests.exceptions import RequestException
from rich.console import Console
from rich_click import argument, command, option

from mrender.docs2md import generate_docs
from mrender.md import Markdown, recursive_read
from mrender.web2md import display_markdown_hierarchically, extract_links, html_to_markdown_with_depth

console = Console()
# Configure logging
log.basicConfig(format='%(asctime)s | %(levelname)s | %(name)s:%(funcName)s:%(lineno)d - %(message)s',
                    level=log.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')

def generate_summary(markdown_content: str):
    summary = []
    for line in markdown_content.split('\n'):
        if line.startswith('# '):
            summary.append(line[2:])  # Remove '# ' prefix
        elif line.startswith('## '):
            summary.append('  ' + line[3:])  # Remove '## ' prefix and add indentation
        elif line.startswith('### '):
            summary.append('    ' + line[4:])  # Remove '### ' prefix and add indentation
    return summary

@command(context_settings={'help_option_names': ['-h', '--help']})
@argument("input", required=False)
@option("--output", "-o", type=click.Path(), help="Output file")
@option("--format", "-f", default="md", help="Output format")
@option("--depth", "-d", default=3, type=int, help="Depth of the output")
@option("--docs", is_flag=True, help="Generate documentation")
@option("--web", is_flag=True, help="Process input as a web URL")
def cli(input: str = None, output: str = None, format: str = "md", depth: int = 3, docs: bool = False, web: bool = False) -> None:
    """Process input file, directory, or web URL and generate output.

        If no input is provided, this help message will be displayed.
        If --web is specified or the input starts with http:// or https://, the input is treated as a web URL.

    Args:
        input (str): Input file, directory, or web URL
        output (str): Output file
        format (str): Output format
        depth (int): Depth of the output
        docs (bool): Generate documentation
        web (bool): Process input as a web URL

    """
    if not input:
        click.echo(click.get_current_context().get_help())
        return

    try:
        log.info(f"Processing input: {input}")
        
        if web or input.startswith(('http://', 'https://')):
            response = requests.get(input, timeout=10)
            response.raise_for_status()
            html_content = response.text
            markdown_content = html_to_markdown_with_depth(html_content, depth)
            links = extract_links(markdown_content)
            if output:
                Path(output).write_text(markdown_content)
                click.echo(f"Web content saved to {output}")
            else:
                display_markdown_hierarchically(markdown_content, depth)
            return

        if docs:
            if not Path(input).exists():
                raise click.ClickException(f"Invalid input: {input}. Path does not exist.")
            
            if Path(input).is_file():
                markdown_content = generate_docs(input)
            elif Path(input).is_dir():
                markdown_content = f"# Package: {Path(input).name}\n\n"
                init_file = Path(input) / "__init__.py"
                if init_file.exists():
                    markdown_content += generate_docs(str(init_file)) + "\n\n"
                for file in Path(input).glob('**/*.py'):
                    if file.name != "__init__.py":
                        markdown_content += generate_docs(str(file)) + "\n\n"
            else:
                raise click.ClickException(f"Invalid input: {input}. Must be a file or directory.")
            
            if output:
                Path(output).write_text(markdown_content)
                click.echo(f"Documentation saved to {output}")
            else:
                click.echo(markdown_content)
            
            # Generate and display summary
            summary = generate_summary(markdown_content)
            click.echo("\nDocumentation Summary:")
            for item in summary:
                click.echo(f"→ {item}")
            return

        if not Path(input).exists():
            raise click.ClickException(f"Invalid input: {input}. Must be a valid file path or directory.")
        data = recursive_read(input)
        if format == "md":
            md = Markdown(data=data, save=output)
            md.stream(depth=depth)
        if links:
            click.secho("\nLinks:")
            for link in links:
                console.print("[link]" + link + "[/link]")
    except requests.exceptions.RequestException as e:
        raise click.ClickException(f"Error fetching web content: {str(e)}") from e
    except click.ClickException:
        raise
    except Exception as e:
        raise click.ClickException(str(e)) from e

if __name__ == '__main__':
    cli()
