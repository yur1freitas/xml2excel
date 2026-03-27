dev:
    uv run src/xml2excel/main.py

fmt:
    uv run ruff format && uv run tombi format

check:
    uv run ty check


build name="xml2excel":
    uv run pyinstaller --onefile -n {{name}} --icon assets/xml2excel.ico --add-data "styles/global.qss:styles/" --add-data "icons/*:icons/" -w src/xml2excel/main.py

husky:
    bun husky

lint-staged:
    bun lint-staged
