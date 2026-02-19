#!/bin/bash
# Mock memotrail command for demo GIF recording
# Usage: source scripts/demo-mock.sh
# This overrides the real memotrail command with scripted output

memotrail() {
    case "$1" in
        stats)
            echo "MemoTrail Stats"
            echo "=============================="
            echo "Sessions indexed:     47"
            echo "Messages stored:      12,830"
            echo "Decisions recorded:   23"
            echo "Chat chunks:          5,241"
            echo "Memory notes:         8"
            ;;
        search)
            shift
            case "$*" in
                *auth*|*JWT*|*login*)
                    echo ""
                    echo "--- Result 1 (score: 0.89) ---"
                    echo "Session: sess_a4f2c831e09b | Project: acme-backend"
                    echo "Time: 2025-12-14 15:32"
                    echo "[user]: Should we use JWT or session-based auth?"
                    echo "[assistant]: JWT is better for your microservices setup."
                    echo "  Stateless tokens avoid shared session stores. I recommend"
                    echo "  short-lived access tokens (15min) + refresh tokens in"
                    echo "  httpOnly cookies."
                    echo "[user]: Makes sense. Let's go with JWT + refresh tokens."
                    echo ""
                    echo "--- Result 2 (score: 0.72) ---"
                    echo "Session: sess_8e1b5d42f7a3 | Project: acme-backend"
                    echo "Time: 2025-12-18 09:15"
                    echo "[user]: Auth middleware is rejecting valid tokens after deploy"
                    echo "[assistant]: Found it — JWT_SECRET env var isn't set in"
                    echo "  production. The fallback key from .env.example is being"
                    echo "  used, which doesn't match tokens signed in staging."
                    echo ""
                    echo "--- Result 3 (score: 0.65) ---"
                    echo "Session: sess_c29f1a76d5e8 | Project: acme-backend"
                    echo "Time: 2026-01-03 11:47"
                    echo "[user]: Add role-based access control to the API"
                    echo "[assistant]: I'll extend the JWT payload with a roles claim"
                    echo "  and add a requireRole() middleware."
                    ;;
                *Redis*|*redis*|*cache*|*caching*)
                    echo ""
                    echo "--- Result 1 (score: 0.91) ---"
                    echo "Session: sess_f7d3a219c4b6 | Project: acme-backend"
                    echo "Time: 2026-01-10 14:22"
                    echo "[user]: API response times are too slow, we need caching"
                    echo "[assistant]: Compared Redis vs Memcached:"
                    echo "  - Redis: data structures, persistence, pub/sub"
                    echo "  - Memcached: simpler, slightly faster for plain k/v"
                    echo "  Recommendation: Redis — you'll need sorted sets for"
                    echo "  the leaderboard feature."
                    echo "[user]: Go with Redis."
                    echo ""
                    echo "--- Result 2 (score: 0.74) ---"
                    echo "Session: sess_2b8e6f41a0d5 | Project: acme-backend"
                    echo "Time: 2026-01-12 10:05"
                    echo "[assistant]: Redis cache layer is live. Average API response"
                    echo "  dropped from 420ms to 35ms. Cache hit rate: 94%."
                    ;;
            esac
            ;;
    esac
}
