#!/bin/bash
# Script to kill runaway Pyright/Python language server processes

echo "=== Killing Cursor Pyright Processes ==="
echo ""

# Function to count processes
count_processes() {
    ps -ax | grep -E "(cursorpyright.*server\.js|run-jedi-language-server\.py)" | grep -v grep | wc -l | tr -d ' '
}

# Show current processes
echo "Current Cursor/Pyright processes: $(count_processes)"
echo ""
echo "Details:"
ps -ax | grep -E "(cursorpyright.*server\.js|run-jedi-language-server\.py)" | grep -v grep | awk '{print $1, $12, $13, $14}' | head -10
echo ""

echo "Attempting to kill processes..."

# Kill Cursor Pyright extension processes with force
echo -n "Killing Cursor Pyright processes... "
pkill -9 -f "anysphere\.cursorpyright.*server\.js"
echo "✓"

# Kill jedi language server processes with force
echo -n "Killing Jedi language server processes... "
pkill -9 -f "run-jedi-language-server\.py"
echo "✓"

# Kill any other pyright-related processes
echo -n "Killing other Pyright processes... "
pkill -9 -f "pyright.*server"
pkill -9 -f "basedpyright"
echo "✓"

# Give processes time to terminate
sleep 2

echo ""
echo "Remaining processes: $(count_processes)"

if [ $(count_processes) -gt 0 ]; then
    echo ""
    echo "⚠️  Some processes are still running. They may have been restarted by Cursor."
    echo "   To prevent auto-restart:"
    echo "   1. Close all Python files in Cursor"
    echo "   2. Disable Python extension temporarily"
    echo "   3. Or restart Cursor completely"
else
    echo "✅ All processes successfully killed!"
fi

echo ""
echo "Done." 