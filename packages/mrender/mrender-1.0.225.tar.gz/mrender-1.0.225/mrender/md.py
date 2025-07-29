import ast
import contextlib
import io
import json
import logging
import asyncio
import time
from pathlib import Path
from types import ModuleType

import click
from lxml.etree import HTML, ElementBase, fromstring,Element
from lxml.html import HTMLParser, document_fromstring
from markdownify import markdownify
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown as RichMarkdown
from rich.text import Text
from typing_extensions import Any,  Self, TypeVar
from mbcore.execute import concurrently
from mbcore.types import deque
logger = logging.getLogger(__name__)


def html(html: str ,ensure_head_body: bool = True, **kw) -> ElementBase:
    parser = HTMLParser()
    value: ElementBase = fromstring(html, parser, **kw)
    if value is None:
        raise ValueError("Invalid HTML")
    if ensure_head_body and value.find('head') is None:
        value.insert(0, Element('head'))
    if ensure_head_body and value.find('body') is None:
        value.append(Element('body'))
    return value

class MarkdownStream:
    live: Live | None
    when: float = 0
    min_delay: float = 0.050
    live_window: int = 6
    mdargs:dict[str,Any]
    def __init__(self, mdargs:dict[str,Any]|None=None):
        self.printed:list[str] = []
        self.mdargs = mdargs or {}

        self.live = Live(Text(""), refresh_per_second=1.0 / self.min_delay)
        self.live.start()

    def __del__(self):
        if self.live:
            with contextlib.suppress(Exception):
                self.live.stop()

    def update(self, text:str, final:bool=False) -> None:
        now = time.time()
        if not final and now - self.when < self.min_delay:
            return
        self.when = now

        string_io = io.StringIO()
        console = Console(file=string_io, force_terminal=True)

        markdown = RichMarkdown(text, **self.mdargs)

        console.print(markdown)
        output = string_io.getvalue()

        lines = output.splitlines(keepends=True)
        num_lines = len(lines)

        if not final:
            num_lines -= self.live_window

        if ( final or num_lines > 0) and self.live:
            num_printed = len(self.printed)

            show = num_lines - num_printed

            if show <= 0:
                return

            show = lines[num_printed:num_lines]
            show = "".join(show)
            show = Text.from_ansi(show)
            self.live.console.print(show)

            self.printed = lines[:num_lines]


        if final and self.live:
            self.live.update(Text(""))
            self.live.stop()
            self.live = None
        elif self.live:
            rest = lines[num_lines:]
            rest = "".join(rest)
            rest = Text.from_ansi(rest)
            self.live.update(rest)
        else:
            raise RuntimeError("Live object is None")

def link_fp(line: str, fn: str | Path, lineno: int, render:bool=True) -> Text | str:
    encoded_path = str(fn) if isinstance(fn, Path) else fn
    link = f"{encoded_path}:{lineno}"
    if render:
        return Text.assemble((line, link))
    return f"[{line}]({link})"


class Markdown:
    """Stream formatted JSON-like text to the terminal with live updates."""

    def __init__(self,
                 data:dict[str,Any]|list[Any]|str|None=None,
                 mdargs:dict[str,Any]|None=None,
                 style:str="default",
                 save:str|None=None,
                 min_delay:float=0.05,
                 live_window:int=6):
        logger.debug(f"Initializing MarkdownStreamer with data: {data}")
        self.data:dict[str,Any]|list[Any]|str|None = data or {}
        self.mdargs:dict[str,Any] = mdargs or {}
        self.style:str = style
        self.console:Console = Console(style=self.style)
        self._save:bool = bool(save)
        self.min_delay:float = min_delay
        self.live_window:int = live_window
        self.last_update_time:float = time.time()
        self.printed_lines:list[str] = []
        self.lines:deque[str] = deque(  self.getlines(self.data))

    @classmethod
    def from_json(cls, json_data: dict[str, Any]|list[Any]|str|None) -> Self:
        """Load JSON data into the MarkdownStreamer."""
        return cls(data=json_data)

    @classmethod
    def from_web(cls, url: str | ElementBase) -> Self:
        from bs4 import BeautifulSoup
        from httpx import get

        from mrender.web2md import html_to_markdown_with_depth
        if not isinstance(url, str):
            return cls(data=html_to_markdown_with_depth(url, 0))
        response = get(url)

        return cls(
            html_to_markdown_with_depth(
                html(
                    BeautifulSoup(response.text,
                                  "html.parser").prettify("utf-8")), 0))

    @classmethod
    def show_pytype(cls, type_: TypeVar) -> None:
        from mrender.render import display_rich_output
        display_rich_output(type_)

    @classmethod
    def from_docs(cls, module_or_path: str | ModuleType | object) -> Self:
        import inspect

        from mrender.docs2md import generate_docs
        if not isinstance(module_or_path, str | ModuleType):
            module_or_path = inspect.getmodule(module_or_path)
        if isinstance(module_or_path, ModuleType):
            module_or_path = module_or_path.__file__
        return cls(generate_docs(module_or_path))

    def put(self, line:dict[str,Any]|list[Any]|str|None=None) -> None:
        self.lines.extend(self.getlines(line))

    def get(self) -> str | None:
        return self.lines.popleft() if self.lines else None

    def getlines(self, data:dict[str,Any]|list[Any]|str|None=None, depth:int=0) -> list[str]:
        """Generate Markdown from JSON with headers based on depth."""
        markdown_lines:list[str] = []
        indent = "  " * depth
        depth = min(3, depth)
        if isinstance(data, dict):
            if "name" in data:
                title = f"\n{indent}{'#' * max(1, depth)} {data['name']}"
                if "brief" in data and data["brief"]:
                    title += f" - {data['brief']}"
                else:
                    title += "\n"
                markdown_lines.append(title)

            # Only process members if we have them and aren't in compact mode
            if "members" in data and isinstance(
                    data["members"],
                    dict) and "brief" in data and data["brief"]:
                for member_name, member_info in data["members"].items():
                    markdown_lines.append(
                        f"{indent}- **{member_name}** {'- ' + member_info['brief'] if 'brief' in member_info else ''}\n"
                    )
                for member_name, _ in data["members"].items():
                    markdown_lines.append(f"{indent}- **{member_name}**\n")

            if "doc" in data and data["doc"]:
                # Format documentation with proper indentation
                doc_lines = str(data["doc"]).split("\n")
                formatted_doc = []
                for line in doc_lines:
                    if line.strip():
                        if line.startswith('@param'):
                            # Format parameter documentation
                            formatted_doc.append(
                                f"{indent}> **{line.strip()}**")
                        else:
                            formatted_doc.append(f"{indent}> {line.strip()}")
                markdown_lines.extend(formatted_doc)
                markdown_lines.append('')

            # Handle return type if available
            if "return_type" in data and data["return_type"]:
                markdown_lines.append(
                    f"{indent}**Returns:** `{data['return_type']}`\n")

            # Handle members and other attributes
            for key, value in data.items():
                if key in ("name", "doc", "return_type"):
                    continue

                if key == "members" and isinstance(value, dict):
                    for _, member_info in value.items():
                        markdown_lines.extend(
                            self.getlines(member_info, depth + 1))
                elif isinstance(value, dict | list):
                    markdown_lines.append(f"\n{indent}- **{key}**:\n")
                    markdown_lines.extend(self.getlines(value, depth + 1))
                elif isinstance(value, str) and value:
                    # Handle file links
                    if key == "path" and "file://" in value:
                        markdown_lines.append(
                            f"{indent}- **{key}**: {value}\n")
                    else:
                        markdown_lines.append(
                            f"{indent}- **{key}**: {value}\n")

        elif isinstance(data, list):
            for item in data:
                markdown_lines.extend(self.getlines(item, depth))
        elif isinstance(data, str):
            markdown_lines.extend(data.split('\n'))
        return markdown_lines

    def format_value(self, key: str, value: Any) -> str:
        """Format the value based on its key and type."""
        code_keys = {"signature", "code"}
        if key.lower() in code_keys and isinstance(value, str):
            return f"```python\n{value}\n```"
        if isinstance(value, str) and (value.startswith("http://")
                                       or value.startswith("https://")):
            return f"[{value}]({value})"

        return str(value)

    def rich(self,  mdargs:dict[str,Any]|None=None) -> RichMarkdown:
        """Render the markdown content using the Rich library."""
        mdargs = mdargs or {}
        self.console.print(RichMarkdown("\n".join(self.lines)))
        return RichMarkdown("\n".join(self.lines), **mdargs)

    def save(self, data:dict[str,Any]|list[Any]|str|None=None, outfile: str | None = None) -> Self:
        """Save the markdown content to a file."""
        data = data or self.data
        data = "\n".join(self.lines)
        if outfile and data:
            _ = Path(outfile).write_text(data)
        return self


    def stream(self, interval:float=0.05, idle_timeout:float=0.5, outfile: str | None = None):
        self._save = bool(outfile)
        pm = MarkdownStream()
        last_len: int = -1
        idle: float = 0.0
        while True:
            markdown_content = "\n".join(self.lines)
            cur_len = len(markdown_content)
            if cur_len != last_len:
                pm.update(markdown_content, final=False)
                last_len = cur_len
                idle = 0.0
            else:
                idle += interval
                if idle >= idle_timeout:
                    break
            time.sleep(interval)
        pm.update(markdown_content, final=True)
        
    @concurrently("event_loop")
    def astream(self, interval:float=0.05, idle_timeout:float=0.5, outfile: str | None = None):
        """Wrapper function that can be properly decorated with concurrently."""
        return self.stream(interval, idle_timeout, outfile)
    

def recursive_read(file:str|Path, include:dict[str,Any]|None=None, depth:int=0, max_depth:int=5) -> dict[str, str]:
    """Recursively read files or directories and return their content as a dictionary."""
    if depth > max_depth and max_depth > 0:
        return {}
    include = include or dict.fromkeys([".json", ".md", ".txt", ".yaml", ".toml", ".py"])
    data:dict[str,Any] = {}
    file_path = Path(file).resolve()
    if file_path.is_file() and file_path.suffix in include and "__pycache__" not in str(file_path) and ".pyc" not in str(file_path):
        logger.info(f"Reading file: {file_path}")
        try:
            content = file_path.read_text()
            if file_path.suffix == ".py":
                data[str(file_path)] = ast.parse(content)
            else:
                data[str(file_path)] = Markdown.from_json(json.loads(content))
        except Exception as e:
            logger.error(f"Error reading file: {file_path}")
            logger.error(e)
    elif file_path.is_dir():
        for sub_path in [p for p in file_path.iterdir() if "__pycache__" not in str(p) and ".pyc" not in str(p)]:
            child = recursive_read(sub_path, include, depth + 1, max_depth)
            data.update(child)
    return data


@click.command("mdstream")
@click.argument("file", type=click.Path(exists=True), required=False)
@click.option("--depth", "-d", default=-1, help="Depth of headers")
@click.option("--save", "-s", help="Save markdown content to a file")
def cli(file:str|None=None, depth:int=-1, save:str|None=None):
    """Stream markdown content from a file."""
    if not file:
        example()
        return
    data = recursive_read(file,depth=0,max_depth=depth)
    md_streamer = Markdown(data=data, save=save)
    md_streamer.stream()


def example() -> None:
    """Run an example with predefined JSON data."""
    json_data = [
        {
            "name": "markdown-to-json",
            "version": "2.1.2",
            "summary": "Markdown to dict and json deserializer",
            "latest_release": "2024-09-20T20:38:56",
            "author": "Nathan Vack",
            "earliest_release": {"version": "1.0.0", "upload_time": "2015-12-10T21:01:13", "requires_python": None},
            "urls": {
                "Bug Tracker": "https://github.com/njvack/markdown-to-json/issues",
                "Change Log": "https://github.com/njvack/markdown-to-json/blob/main/CHANGELOG.md",
            },
            "description": "# Markdown to JSON converter\n## Description\nA simple tool...",
            "requires_python": ">=3.8",
        }
    ]
    md_streamer = Markdown(data=json_data)
    f = md_streamer.astream()
    print(f"Starting stream")
    for i in range(10):
        new_json_data = [
            {
                "name": f"item {i}",
                "version": f"2.1.2.{i}",

            }
        ]
        md_streamer.put(new_json_data)
    print(f"Waiting for stream to finish")
    f.result()


    


if __name__ == "__main__":
    cli()
