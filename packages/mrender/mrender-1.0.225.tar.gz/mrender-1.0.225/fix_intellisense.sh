#!/bin/bash
# Fix Cursor/VSCode IntelliSense issues

echo "=== Fixing IntelliSense Issues ==="
echo ""

# Kill language server processes
echo "1. Killing language server processes..."
pkill -9 -f "anysphere\.cursorpyright.*server\.js"
pkill -9 -f "run-jedi-language-server\.py"
pkill -9 -f "pyright.*server"
echo "   ✓ Done"

# Clear Python cache
echo ""
echo "2. Clearing Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
echo "   ✓ Done"

# Clear Pylance cache if it exists
echo ""
echo "3. Clearing Pylance cache..."
rm -rf .vscode/.pylance-cache 2>/dev/null || true
echo "   ✓ Done"

echo ""
echo "✅ Complete! Please reload the window in Cursor (Cmd+R or Ctrl+R)"
echo "" 