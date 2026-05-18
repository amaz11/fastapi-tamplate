#!/usr/bin/env bash
# Create a new project from this template.
# Usage: ./scripts/new-project.sh <target-directory> [display-name]
set -euo pipefail

TEMPLATE_NAME="FastAPI Template"
TEMPLATE_SLUG="fastapi-template"

usage() {
  cat <<EOF
Usage: $(basename "$0") <target-directory> [display-name]

Examples:
  $(basename "$0") ../billing-api "Billing API"
  $(basename "$0") ../shop-backend

Creates a copy of the template, renames placeholders, generates .env with a new SECRET_KEY.
EOF
  exit 1
}

[[ $# -ge 1 ]] || usage

TARGET_DIR=$(cd "$(dirname "$1")" && pwd)/$(basename "$1")
DISPLAY_NAME="${2:-}"
SLUG=""

if [[ -z "$DISPLAY_NAME" ]]; then
  DISPLAY_NAME=$(basename "$TARGET_DIR" | sed 's/-/ /g; s/_/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2));}1')
fi

SLUG=$(echo "$DISPLAY_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g; s/--*/-/g; s/^-//; s/-$//')

if [[ -e "$TARGET_DIR" ]]; then
  echo "Error: target already exists: $TARGET_DIR" >&2
  exit 1
fi

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

echo "Creating project at: $TARGET_DIR"
echo "Display name: $DISPLAY_NAME"
echo "Slug: $SLUG"

mkdir -p "$TARGET_DIR"

rsync -a \
  --exclude '.git' \
  --exclude '.venv' \
  --exclude 'venv' \
  --exclude '__pycache__' \
  --exclude '.pytest_cache' \
  --exclude '.ruff_cache' \
  --exclude '.mypy_cache' \
  --exclude '*.db' \
  --exclude '.env' \
  --exclude 'htmlcov' \
  --exclude '.coverage' \
  --exclude 'dist' \
  --exclude 'build' \
  --exclude '*.egg-info' \
  "$ROOT_DIR/" "$TARGET_DIR/"

replace_in_files() {
  local search="$1"
  local replace="$2"
  if [[ "$OSTYPE" == "darwin"* ]]; then
    find "$TARGET_DIR" -type f \( \
      -name '*.py' -o -name '*.md' -o -name '*.yml' -o -name '*.yaml' \
      -o -name '*.ini' -o -name '*.toml' -o -name '*.sh' -o -name 'Makefile' \
      -o -name '.env.example' -o -name '.env.docker.example' \
    \) -exec sed -i '' "s|${search}|${replace}|g" {} +
  else
    find "$TARGET_DIR" -type f \( \
      -name '*.py' -o -name '*.md' -o -name '*.yml' -o -name '*.yaml' \
      -o -name '*.ini' -o -name '*.toml' -o -name '*.sh' -o -name 'Makefile' \
      -o -name '.env.example' -o -name '.env.docker.example' \
    \) -exec sed -i "s|${search}|${replace}|g" {} +
  fi
}

replace_in_files "$TEMPLATE_NAME" "$DISPLAY_NAME"
replace_in_files "$TEMPLATE_SLUG" "$SLUG"
replace_in_files "my-fastapi" "$SLUG"

SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(48))")

cp "$TARGET_DIR/.env.example" "$TARGET_DIR/.env"
if [[ "$OSTYPE" == "darwin"* ]]; then
  sed -i '' "s|^SECRET_KEY=.*|SECRET_KEY=${SECRET_KEY}|" "$TARGET_DIR/.env"
  sed -i '' "s|^APP_NAME=.*|APP_NAME=${DISPLAY_NAME}|" "$TARGET_DIR/.env"
else
  sed -i "s|^SECRET_KEY=.*|SECRET_KEY=${SECRET_KEY}|" "$TARGET_DIR/.env"
  sed -i "s|^APP_NAME=.*|APP_NAME=${DISPLAY_NAME}|" "$TARGET_DIR/.env"
fi

chmod +x "$TARGET_DIR/scripts/new-project.sh" 2>/dev/null || true
chmod +x "$TARGET_DIR/docker/entrypoint.sh" 2>/dev/null || true

cat > "$TARGET_DIR/.template-origin" <<EOF
Generated from FastAPI template on $(date -u +"%Y-%m-%dT%H:%M:%SZ")
Display name: ${DISPLAY_NAME}
Slug: ${SLUG}
EOF

echo ""
echo "Done. Next steps:"
echo "  cd $TARGET_DIR"
echo "  make install    # or: pip install -r requirements.txt"
echo "  make migrate"
echo "  make seed"
echo "  uvicorn app.main:app --reload"
echo ""
echo "Optional:"
echo "  git init && git add . && git commit -m \"Initial commit from template\""
echo "  make up         # Docker + MySQL"
echo ""
echo "Before production: see PRODUCTION.md"
