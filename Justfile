set shell:= ['cmd.exe', "/c"]

check:
    ruff check *.py
fix:
    ruff check *.py --fix
    black *.py
    isort *.py
run:
    python main.py
