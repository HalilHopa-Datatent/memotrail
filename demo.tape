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

# Load mock silently
Hide
Type "cd /Users/halilhopa/Documents/GitHub/Memotrail && source scripts/demo-mock.sh && hash -r && clear"
Enter
Sleep 2s
Show

# --- Stats ---
Sleep 500ms
Type "memotrail stats"
Sleep 400ms
Enter
Sleep 3s

# --- Search: Redis decision ---
Type@55ms 'memotrail search "why did we choose Redis for caching"'
Sleep 400ms
Enter
Sleep 8s

# --- Search: race condition ---
Type@55ms 'memotrail search "how do we handle inventory race conditions"'
Sleep 400ms
Enter
Sleep 8s

# --- Connect to Claude Code ---
Type "# Add to Claude Code — one command:"
Enter
Sleep 500ms
Type "claude mcp add memotrail -- memotrail serve"
Sleep 1.5s
Enter
Sleep 3s
