import re
from inspect import cleandoc, signature

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

from mrender.docs2md import generate_docs as generate_markdown


def display_class_methods(cls, markdown:bool=False):

    if markdown:
        return generate_markdown(cls)
    return display_rich_output(cls)



# The rest of the code remains the same

def display_rich_output(cls) -> None:
    console = Console()

    # Class header and docstring
    class_doc = cleandoc(cls.__doc__)
    parts = re.split(r"(Example:.*?)(?=\n\n|\Z)", class_doc, flags=re.DOTALL)

    class_desc = parts[0].strip()
    examples = " ".join(parts[1:]).strip()

    # Display class description
    console.print(Panel(Markdown(f"# {cls.__name__}\n\n{class_desc}"), expand=False, border_style="yellow"))
    console.print()

    # Display examples
    if examples:
        console.print(
            Panel(
                Syntax(examples, "python", theme="monokai", background_color="default"),
                title="Examples",
                expand=False,
                border_style="yellow",
            )
        )
        console.print()

    # Method header
    header = Table(show_header=True, header_style="bold magenta", expand=True)
    header.add_column("Method", style="cyan", width=20)
    header.add_column("Signature", style="green", width=50)
    header.add_column("Description", style="yellow", width=30)
    console.print(header)

    for name, method in cls.__dict__.items():
        if callable(method) and not name.startswith("__"):
            method_table = Table(show_header=False, expand=True, border_style="bright_blue")
            method_table.add_column("Method", style="cyan", width=20)
            method_table.add_column("Signature", style="green", width=50)
            method_table.add_column("Description", style="yellow", width=30)

            sig = signature(method)
            doc = cleandoc(method.__doc__) if method.__doc__ else "No docstring provided."

            brief_desc = doc.split("\n")[0]
            doc_link = create_doc_link(cls, name)

            # Enhance signature contrast
            sig_text = str(sig)
            sig_text = re.sub(r"(\w+):", r"[bold yellow]\1[/bold yellow]:", sig_text)
            sig_text = re.sub(r": (\w+)", r": [bold green]\1[/bold green]", sig_text)
            sig_text = re.sub(r"(->.*)", r"[bold red]\1[/bold red]", sig_text)

            # Wrap long signatures
            wrapped_sig = Text.from_markup(sig_text)
            wrapped_sig.wrap(console, width=48)

            full_desc = Text.assemble(Text(brief_desc), "\n\n", Text("Docs", style="link blue underline"))
            full_desc.stylize(f"link {doc_link}")
            full_desc.wrap(console=console, width=28)

            method_table.add_row(Text(name, style="bold cyan"), wrapped_sig, full_desc)

            console.print(method_table)
            console.print()  # Add a small gap between method rows

def create_doc_link(cls, method_name) -> str:
    return f"#{cls.__name__.lower()}-{method_name.lower()}"
