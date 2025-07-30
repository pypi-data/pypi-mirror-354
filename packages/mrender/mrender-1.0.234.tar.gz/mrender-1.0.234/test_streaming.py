#!/usr/bin/env python3
"""Test the Markdown streaming functionality."""

from mrender.md import Markdown

# Test with simple data
test_data = [
    {"name": "pytest-markdown", "version": "1.0.2", "summary": "Test markdown in pytest"},
    {"name": "pytest-markdown-docs", "version": "0.5.0", "summary": "Documentation testing with markdown"},
]

print("Testing Markdown streaming...")
md = Markdown(test_data)
md.stream(interval=0.5, idle_timeout=2.0)
print("\nStreaming complete!") 