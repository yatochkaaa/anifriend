#!/usr/bin/env bash
file=$(python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('file_path',''))" 2>/dev/null)
[[ "$file" == *.py ]] && backend/.venv/bin/ruff format "$file" 2>/dev/null
exit 0
