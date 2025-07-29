import importlib
import inspect
from pathlib import Path
import pydoc
from types import ModuleType
from typing import Any, Union, Type

def bfs_explore_module(
    module: ModuleType, depth: int = 1, include_signatures: bool = True, include_docstrings: bool = True, max_depth: int = 3,
) -> list[dict[str, str | dict[str, str]]]:
    """Explore the module using BFS and extract signatures/docstrings up to a certain depth."""
    if depth > max_depth:
        return []
    result = []

    def explore_item(item, current_depth: int):
        if current_depth > depth:
            return

        item_dict = {"name": item.__name__}

        # Try to extract the signature if needed
        if include_signatures and (inspect.isfunction(item) or inspect.isclass(item)):
            try:
                item_dict["signature"] = str(inspect.signature(item))
            except (ValueError, TypeError):
                item_dict["signature"] = None

        if include_docstrings:
            doc = inspect.getdoc(item)
            if doc:
                doc_head, _ = pydoc.splitdoc(doc)  # Only use the synopsis (first line)
                item_dict["docstring"] = doc_head

        result.append(item_dict)

        if inspect.isclass(item):
            for attr_name, attr_value in inspect.getmembers(item):
                if inspect.isfunction(attr_value) or inspect.isclass(attr_value):
                    explore_item(attr_value, current_depth + 1)

    for attr_name, attr_value in inspect.getmembers(module):
        if inspect.isfunction(attr_value) or inspect.isclass(attr_value):
            explore_item(attr_value, 1)

    return result


def extract_docstring_from_object(
    obj: str | ModuleType | type | None,
    depth: int = 0,
    include_signatures: bool = True,
    include_docstrings: bool = True,
) -> list[dict[str, str | dict[str, str]]]:
    """Extract docstrings and signatures from a module or class with BFS and depth control."""
    out = []
    queue = [obj]
    try:
        while queue:
            obj = queue.pop(0)
            # If it's a module name as string, import it
            if isinstance(obj, str):
                obj = importlib.import_module(obj)
                filepath = obj.__file__

                def walk_the_sibling_paths(filepath: str):
                    # walk the sibling paths
                    for p in Path(filepath).parent.iterdir():
                        if p.suffix == ".py":
                            queue.append(p)
                        elif p.is_dir():
                            for p in p.iterdir():
                                if p.suffix == ".py":
                                    queue.append(p)
             
                walk_the_sibling_paths(filepath)
            out.extend(bfs_explore_module(obj, depth+1, include_signatures, include_docstrings,max_depth=depth))
      
        return out

    except (ImportError, AttributeError, Exception) as e:
        raise ImportError(f"Could not import {obj}: {e}") from e


# Now, the result is structured as a list of dictionaries for Markdown generation
if __name__ == "__main__":
    module_result = extract_docstring_from_object(
        "pydantic", depth=1, include_signatures=True, include_docstrings=False
    )
    from mrender.md import Markdown
    # You can now pass this to your existing Markdown generator
    Markdown(module_result).stream()
