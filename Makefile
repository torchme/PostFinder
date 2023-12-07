VENV := .venv

PROJECT := PostFinder
TESTS := tests

# Prepare

.venv:
	poetry install --no-root
	poetry check

setup: .venv

# Clean

clean:
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf $(VENV)

# Format

isort_fix: .venv
	poetry run isort $(PROJECT) $(TESTS)

black_fix: .venv
	poetry run black $(PROJECT) $(TESTS)

format: isort_fix black_fix

# Lint

isort: .venv
	poetry run isort --check $(PROJECT) $(TESTS)

.black: .venv
	poetry run black --check --diff $(PROJECT) $(TESTS)

flake: .venv
	poetry run flake8 $(PROJECT) $(TESTS)

mypy: .venv
	poetry run mypy $(PROJECT) $(TESTS)

pylint: .venv
	poetry run pylint $(PROJECT) $(TESTS)

lint: isort .black flake mypy pylint

# Test

.pytest: .venv
	poetry run pytest $(TESTS) -vv

test: .pytest

# All

all: setup format lint test

.DEFAULT_GOAL = all
