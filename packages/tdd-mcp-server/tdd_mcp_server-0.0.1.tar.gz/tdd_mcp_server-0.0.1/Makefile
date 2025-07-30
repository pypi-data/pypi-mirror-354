# -*- coding: utf-8 -*-
.PHONY: clean build bump deploy black blackcheck imports lint typecheck check_no_typing check test tests coverage xmlcov check_ci deps devdeps

clean:
	rm -rf __pycache__ build/ dist/ *.egg-info/ .coverage htmlcov

build: clean
	python -m build

bump:
	./scripts/bump-version.py

deploy: build
	./scripts/deploy.sh

black:
	black .

blackcheck:
	black --check .

lint:
	ruff check

typecheck:
	mypy tdd_mcp_server

check_no_typing:
	pytest

check: blackcheck lint typecheck check_no_typing

test: check
tests: check

deps:
	pip install -e .[dev]

