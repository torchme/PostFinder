# 🔎 POSTFINDER

---
## 1. Install

### python3.8

```
pip install poetry

pip install --upgrade pip

poetry install
```

### pre-commit

```
pre-commit
```

or

```
pre-commit install
```

## 2. Run
### Add .env file with secret keys
* API_ID
* API_HASH
* TELEGRAM_BOT_TOKEN
* PROXY_API_KEY

**For database connection:** (with examples)
* DB_USER=postgres
* DB_PASS=postgres
* DB_HOST=localhost
* DB_PORT=5432
* DB_NAME=postfinder

**For docker compose:**
* POSTGRES_DB=postfinder
* POSTGRES_USER=postgres
* POSTGRES_PASSWORD=postgres

### Add .env-docker file with secret keys (DB_HOST is different from .env file)
* API_ID
* API_HASH
* TELEGRAM_BOT_TOKEN
* PROXY_API_KEY

**For database connection:** (with examples)
* DB_USER=postgres
* DB_PASS=postgres
* DB_HOST=postgres_db
* DB_PORT=5432
* DB_NAME=postfinder

**For docker compose:**
* POSTGRES_DB=postfinder
* POSTGRES_USER=postgres
* POSTGRES_PASSWORD=postgres

### Start bot

```python
bash run_bot.sh
```

or

```
python -m src.app.bot
```

## 3. Run With Docker
```
docker-compose -f docker/docker-compose.yaml build
docker-compose -f docker/docker-compose.yaml up
```

## 4. Setup PostgreSQL with Docker
```
docker-compose -f docker/docker-compose.yaml build migrations
docker-compose -f docker/docker-compose.yaml up migrations
```
