#!/bin/bash
# Export UV dependencies to requirements.txt for Firebase Functions deployment
# Firebase requires a requirements.txt file, but we use UV for local development

set -e

cd "$(dirname "$0")"

echo "📦 Exporting UV dependencies to requirements.txt..."

# Export dependencies from pyproject.toml using uv
uv pip compile pyproject.toml -o requirements.txt --quiet

echo "✅ requirements.txt updated successfully!"
echo ""
echo "Dependencies exported:"
cat requirements.txt
