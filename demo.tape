# MemoTrail Demo
# Generate: vhs demo.tape

Output demo.gif

Set Shell "bash"
Set FontSize 15
Set Width 1100
Set Height 650
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

# --- Scene 1: Install ---
Sleep 500ms
Type "pip install memotrail"
Sleep 400ms
Enter
Sleep 4s

Type "clear"
Enter
Sleep 500ms

# --- Scene 2: Connect to Claude Code ---
Type "claude mcp add memotrail -- memotrail serve"
Sleep 400ms
Enter
Sleep 3s

Type "clear"
Enter
Sleep 500ms

# --- Scene 3: Stats ---
Type "memotrail stats"
Sleep 400ms
Enter
Sleep 3s

Type "clear"
Enter
Sleep 500ms

# --- Scene 4: Search ---
Type@55ms 'memotrail search "why did we choose Redis for caching"'
Sleep 400ms
Enter
Sleep 8s

Type "clear"
Enter
Sleep 500ms

# --- Scene 5: Save memory ---
Type@55ms 'memotrail save-memory "We use Redis for caching with 5-min TTL"'
Sleep 400ms
Enter
Sleep 3s

Type "clear"
Enter
Sleep 500ms

# --- Scene 6: Duplicate detection (consolidation) ---
Type@55ms 'memotrail save-memory "We use Redis for caching with 5-min TTL"'
Sleep 400ms
Enter
Sleep 3s

Type "clear"
Enter
Sleep 500ms

# --- Scene 7: Contradiction detection ---
Type@55ms 'memotrail save-memory "Switched from Redis to Memcached for caching"'
Sleep 400ms
Enter
Sleep 3s
