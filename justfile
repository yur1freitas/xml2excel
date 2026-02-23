dev:
    uv run src/xml2excel/main.py

fmt:
    uv run ruff format && uv run tombi format

check:
    uv run ty check

build:
    uv run pyinstaller --onefile -n xml2excel --icon assets/xml2excel.ico -w src/xml2excel/main.py

husky:
    bun husky

lint-staged:
    bun lint-staged
