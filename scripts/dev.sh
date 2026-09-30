
#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
ENV_FILE="$BACKEND_DIR/.env"
COMMAND="${1:-help}"

if docker compose version >/dev/null 2>&1; then
  COMPOSE=(docker compose)
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE=(docker-compose)
else
  printf 'Docker Compose is required (install the Docker Compose v2 plugin).\n' >&2
  exit 1
fi
COMPOSE+=(--env-file "$ENV_FILE" -f "$ROOT_DIR/compose.yaml")

if [[ ! -f "$ENV_FILE" ]]; then
  printf 'Missing backend environment file: %s\n' "$ENV_FILE" >&2
  exit 1
fi

run_migration() {
  "${COMPOSE[@]}" up -d --wait postgres
  "${COMPOSE[@]}" run --rm --no-deps -e PG_HOST=postgres api alembic "$@"
}

case "$COMMAND" in
  up)
    "${COMPOSE[@]}" up --build -d
    printf 'API:      http://localhost:8000\n'
    printf 'Docs:     http://localhost:8000/docs\n'
    printf 'Frontend: http://localhost:3000\n'
    ;;
  down)
    "${COMPOSE[@]}" down
    ;;
  logs)
    "${COMPOSE[@]}" logs -f api
    ;;
  migrate-upgrade)
    run_migration upgrade head
    ;;
  migrate-downgrade)
    run_migration downgrade -1
    ;;
  migrate-create)
    shift || true
    MESSAGE="${*:-new_migration}"
    run_migration revision --autogenerate -m "$MESSAGE"
    ;;
  psql)
    "${COMPOSE[@]}" exec postgres sh -lc 'exec psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"'
    ;;
  help|-h|--help)
    printf '%s\n' \
      'Usage: ./scripts/dev.sh <command>' \
      '' \
      '  up                Build and start the stack' \
      '  down              Stop the stack' \
      '  logs              Tail API logs' \
      '  migrate-upgrade   Apply pending Alembic migrations' \
      '  migrate-downgrade Revert the last migration' \
      '  migrate-create    Autogenerate a migration (pass a message)' \
      '  psql              Open a psql shell in the Postgres container'
    ;;
  *)
    printf 'Unknown command: %s\n' "$COMMAND" >&2
    printf 'Run ./scripts/dev.sh help for available commands.\n' >&2
    exit 2
    ;;
esac