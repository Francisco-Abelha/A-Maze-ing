PYTHON := python3
CONFIG := config.txt

.PHONY: run debug install clean lint lint-strict

run:
	$(PYTHON) a_maze_ing.py $(CONFIG)

debug:
	$(PYTHON) -m pdb a_maze_ing.py $(CONFIG)

install:
	$(PYTHON) -m pip install flake8 mypy

clean:
	rm -rf __pycache__ .mypy_cache

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict