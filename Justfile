set shell:= ['cmd.exe', "/c"]

check:
    ruff check *.py
fix:
    ruff check *.py --fix
    black *.py
    isort main.py modules.py
run:
    python main.py
