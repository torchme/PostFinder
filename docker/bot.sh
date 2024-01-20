#!/bin/bash

poetry run alembic upgrade head

poetry run python -m src.app.bot
