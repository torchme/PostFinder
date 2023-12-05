VENV := .venv

PROJECT := src
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


black_fix:
	poetry run black $(PROJECT) $(TESTS)

format: isort_fix black_fix


# Lint

isort: .venv
	poetry run isort --check $(PROJECT) $(TESTS)

.black:
	poetry run black --check --diff $(PROJECT) $(TESTS)

mypy: .venv
	poetry run mypy $(PROJECT) $(TESTS)

pylint: .venv
	poetry run pylint $(PROJECT) $(TESTS)

lint: isort mypy pylint


# Test

.pytest:
	poetry run pytest $(TESTS)

test: .venv .pytest


# All

all: setup format lint test run

.DEFAULT_GOAL = all
