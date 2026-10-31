#!/usr/bin/env bash
set -euo pipefail
REPO="AIPMAndy/chinese-x-creators"
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
command -v git >/dev/null || { echo '请先安装 Git'; exit 1; }
command -v gh >/dev/null || { echo '请先安装 GitHub CLI: https://cli.github.com/'; exit 1; }
command -v python3 >/dev/null || { echo '需要 Python 3.9+'; exit 1; }
cd "$BASE_DIR"
python3 scripts/validate_research.py
python3 scripts/build.py
python3 scripts/build_cases.py
python3 -m unittest discover -s tests -v
gh auth status >/dev/null || { echo '请先执行 gh auth login'; exit 1; }
# Avoid non-fast-forward conflict for a repository initialized via GitHub UI or connector.
if ! gh repo view "$REPO" >/dev/null 2>&1; then
  gh repo create "$REPO" --public --description='中文 X 千万级商业化研究库：真实案例、收入证据分级和开源研究 SOP'
fi
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
gh repo clone "$REPO" "$TMP_DIR/repo"
python3 - "$BASE_DIR" "$TMP_DIR/repo" <<'PY'
import os, pathlib, shutil, sys
src, dest = [pathlib.Path(p).resolve() for p in sys.argv[1:]]
for p in src.rglob('*'):
    rel = p.relative_to(src)
    if any(part in {'.git', '__pycache__', '.pytest_cache', '.DS_Store'} for part in rel.parts):
        continue
    target = dest / rel
    if p.is_dir():
        target.mkdir(parents=True, exist_ok=True)
    elif p.is_file():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, target)
PY
git -C "$TMP_DIR/repo" add -A
if ! git -C "$TMP_DIR/repo" diff --cached --quiet; then
  git -C "$TMP_DIR/repo" -c user.name="AI Chief Andy" -c user.email="noreply@users.noreply.github.com" commit -m 'feat: publish complete research library v2.0'
  git -C "$TMP_DIR/repo" push origin HEAD:main
else
  echo '仓库内容已经是最新，无需提交。'
fi
echo "仓库：https://github.com/$REPO"
echo '如未启用 Pages：Settings → Pages → Deploy from a branch → main → /docs → Save'
