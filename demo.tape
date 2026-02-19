# MemoTrail Demo
# Generate: vhs demo.tape

Output demo.gif

Set Shell "bash"
Set FontSize 15
Set Width 1100
Set Height 600
Set Theme "Catppuccin Mocha"
Set Padding 20
Set TypingSpeed 40ms
Set WindowBar Colorful
Set WindowBarSize 40

# Load mock memotrail function silently
Hide
Type "source scripts/demo-mock.sh"
Enter
Sleep 500ms
Type "clear"
Enter
Sleep 500ms
Show

# --- Stats ---
Sleep 500ms
Type "memotrail stats"
Sleep 400ms
Enter
Sleep 3s

# --- Search: authentication ---
Type 'memotrail search "JWT authentication decision"'
Sleep 400ms
Enter
Sleep 7s

# --- Search: Redis ---
Type 'memotrail search "why did we choose Redis for caching"'
Sleep 400ms
Enter
Sleep 7s

# --- Connect to Claude Code ---
Type "# Connect to Claude Code"
Enter
Sleep 800ms
Type "claude mcp add memotrail -- memotrail serve"
Sleep 2s

Enter
Sleep 2s
Type "# Your AI now remembers everything."
Enter
Sleep 3s
