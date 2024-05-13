SHELL := /bin/bash

install:
	pip install poetry
	poetry install

auth:
	poetry run prefect cloud login --key $(PREFECT_API_KEY) --workspace $(PREFECT_WORKSPACE_ID)

run:
	poetry run sh src/dags/prefect.sh
