#!/bin/bash
# Mock memotrail command for demo GIF recording
# Based on realistic e-commerce API development sessions
# Usage: source scripts/demo-mock.sh

memotrail() {
    case "$1" in
        stats)
            echo "MemoTrail Stats"
            echo "=============================="
            echo "Sessions indexed:     16"
            echo "Messages stored:      4,590"
            echo "Decisions recorded:   12"
            echo "Chat chunks:          1,852"
            echo "Memory notes:         5"
            ;;
        search)
            shift
            query="$*"
            case "$query" in
                *[Rr]edis*|*cach*)
                    echo ""
                    echo "--- Result 1 (score: 0.92) ---"
                    echo "Session: sess_e4a1b832c7f9 | Project: ecommerce-api"
                    echo "Time: 2026-01-29 09:18"
                    echo "[user]: Should we use Redis for caching the product catalog?"
                    echo "  We expect heavy read traffic."
                    echo "[assistant]: For heavy read traffic on product catalog, Redis"
                    echo "  is the right call. Here's the caching strategy:"
                    echo "  1. Cache-aside pattern: check Redis first, fallback to Postgres"
                    echo "  2. TTL of 5 minutes for product listings"
                    echo "  3. Instant invalidation when product is updated"
                    echo "  4. Redis sorted sets for category-based rankings"
                    echo "[user]: Perfect. Let's go with that."
                    echo ""
                    echo "--- Result 2 (score: 0.78) ---"
                    echo "Session: sess_a2c8d915f3b1 | Project: ecommerce-api"
                    echo "Time: 2026-02-05 11:00"
                    echo "[user]: We're getting hammered by scrapers on product endpoints."
                    echo "[assistant]: Let's use slowapi with Redis as the rate limiting"
                    echo "  backend — since we already have Redis running for caching."
                    echo "  Product browsing: 30/min, auth endpoints: 5/min."
                    echo ""
                    echo "--- Result 3 (score: 0.71) ---"
                    echo "Session: sess_b7f4e621d8a3 | Project: ecommerce-api"
                    echo "Time: 2026-02-10 15:00"
                    echo "[assistant]: Redis cache for popular searches — top 100 queries"
                    echo "  cached for 2 min. Combined with cursor-based pagination, this"
                    echo "  should bring search response from ~800ms to under 100ms."
                    ;;
                *race*|*inventory*|*stock*)
                    echo ""
                    echo "--- Result 1 (score: 0.94) ---"
                    echo "Session: sess_d5f2a841b9c7 | Project: ecommerce-api"
                    echo "Time: 2026-02-02 14:30"
                    echo "[user]: We have a race condition. Two users are buying the last"
                    echo "  item in stock simultaneously. How do we handle this?"
                    echo "[assistant]: Classic inventory race condition. Use SELECT FOR"
                    echo "  UPDATE to lock the row during the transaction:"
                    echo ""
                    echo "  async def reserve_stock(variant_id, quantity):"
                    echo "      async with db.begin():"
                    echo "          variant = await db.execute("
                    echo "              select(ProductVariant)"
                    echo "              .with_for_update()  # Row-level lock"
                    echo "          )"
                    echo "          if variant.stock_quantity < quantity:"
                    echo "              raise InsufficientStockError()"
                    echo ""
                    echo "  Decision: PostgreSQL SELECT FOR UPDATE for inventory to"
                    echo "  prevent overselling."
                    ;;
                *deploy*|*infra*|*hosting*|*aws*|*ecs*)
                    echo ""
                    echo "--- Result 1 (score: 0.90) ---"
                    echo "Session: sess_c3e9f712a4d6 | Project: ecommerce-api"
                    echo "Time: 2026-02-17 16:00"
                    echo "[user]: Should we deploy on AWS ECS or a simple VPS with"
                    echo "  Docker Compose?"
                    echo "[assistant]: For your current stage, Docker Compose on a VPS:"
                    echo "  - ECS adds complexity (load balancers, task definitions)"
                    echo "  - Costs \$150+/month minimum vs \$24/month on Hetzner"
                    echo "  - You're not at the scale that needs auto-scaling yet"
                    echo "  Decision: Docker Compose on Hetzner VPS (\$24/month)."
                    echo "  Migrate to ECS when you hit 70%+ CPU consistently."
                    echo ""
                    echo "--- Result 2 (score: 0.68) ---"
                    echo "Session: sess_a8b3c214e5f7 | Project: ecommerce-api"
                    echo "Time: 2026-02-12 09:30"
                    echo "[assistant]: Webhook delivery using Celery for async processing."
                    echo "  3 retries with exponential backoff (1min, 5min, 30min)."
                    echo "  Payloads signed with HMAC-SHA256."
                    ;;
                *auth*|*JWT*|*jwt*|*login*|*token*)
                    echo ""
                    echo "--- Result 1 (score: 0.91) ---"
                    echo "Session: sess_e4a1b832c7f9 | Project: ecommerce-api"
                    echo "Time: 2026-01-29 09:25"
                    echo "[user]: Let's implement JWT authentication. I want access"
                    echo "  tokens and refresh tokens."
                    echo "[assistant]: Dual-token JWT auth system:"
                    echo "  - Access token: 15 min expiry, used for API requests"
                    echo "  - Refresh token: 7 day expiry, httponly cookie"
                    echo "  - Token rotation: new refresh token on each refresh"
                    echo "  - Password hashing with bcrypt via passlib"
                    echo ""
                    echo "--- Result 2 (score: 0.76) ---"
                    echo "Session: sess_e4a1b832c7f9 | Project: ecommerce-api"
                    echo "Time: 2026-01-29 10:45"
                    echo "[user]: Getting CORS errors from the frontend."
                    echo "[assistant]: allow_credentials=True is required for cookies,"
                    echo "  and you can't use allow_origins=[\"*\"] with credentials."
                    echo "  You must specify exact origins."
                    ;;
                *)
                    echo ""
                    echo "--- Result 1 (score: 0.65) ---"
                    echo "Session: sess_e4a1b832c7f9 | Project: ecommerce-api"
                    echo "Time: 2026-01-29 09:15"
                    echo "[assistant]: Clean FastAPI project structure with routers/,"
                    echo "  models/, schemas/, and core/ directories. PostgreSQL with"
                    echo "  SQLAlchemy async, JWT tokens for auth."
                    ;;
            esac
            ;;
    esac
}
