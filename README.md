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
### Add .env and .env-docker file with secret keys
* Contact @redpf for keys

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
