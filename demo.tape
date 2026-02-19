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

# Setup PATH silently
Hide
Type "export PATH=$HOME/.local/bin:$PATH"
Enter
# Pre-warm the embedding model so search is faster
Type 'memotrail search "warmup" 2>/dev/null 1>/dev/null'
Enter
Sleep 15s
Type "clear"
Enter
Sleep 500ms
Show

# --- Stats ---
Sleep 500ms
Type "# Check indexed sessions"
Enter
Sleep 800ms
Type "memotrail stats 2>/dev/null"
Sleep 400ms
Enter
Sleep 3s

# --- Search 1 ---
Type "# Search past conversations"
Enter
Sleep 800ms
Type@60ms 'memotrail search "chunking embedding architecture" 2>/dev/null'
Sleep 400ms
Enter
Sleep 6s

# --- Search 2 ---
Type "# Try another query"
Enter
Sleep 800ms
Type@60ms 'memotrail search "project structure modules" 2>/dev/null'
Sleep 400ms
Enter
Sleep 6s

# --- Connect ---
Type "# Connect to Claude Code — one command"
Enter
Sleep 800ms
Type@50ms "claude mcp add memotrail -- memotrail serve"
Sleep 2s
Enter
Sleep 1s

Type ""
Enter
Sleep 500ms
Type "# Your AI now remembers everything."
Enter
Sleep 3s
