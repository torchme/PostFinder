# 🔎 POSTFINDER

---
![t.me/postfinder](https://img.shields.io/badge/Telegram-1F1F1F?style=for-the-badge&logo=telegram&logoColor=white) ![ChatGPT API](https://img.shields.io/badge/ChatGPT-1F1F1F?style=for-the-badge&logo=openai&logoColor=white) ![ChatGPT API](https://img.shields.io/badge/ChatGPT-1F1F1F?style=for-the-badge&logo=openai&logoColor=white) ![Chroma DB](https://img.shields.io/badge/Chroma_DB-1F1F1F?style=for-the-badge&logo=chromadb&logoColor=white) ![Python](https://img.shields.io/badge/Python-1F1F1F?style=for-the-badge&logo=python&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-1F1F1F?style=for-the-badge&logo=docker&logoColor=white) ![GitBook](https://img.shields.io/badge/GitBook-1F1F1F?style=for-the-badge&logo=gitbook&logoColor=white)

![Static Badge](https://img.shields.io/badge/python-3.10+stable-1f1f1f?style=flat&labelColor=lightblue&color=1f1f1f) ![Pre-install Test](https://github.com/torchme/PostFinder/actions/workflows/python-app.yml/badge.svg?branch=main) ![GitHub Repo stars](https://img.shields.io/github/stars/torchme/PostFinder?style=flat&labelColor=lightblue&color=1f1f1f.svg) ![Github Watchers](https://img.shields.io/github/watchers/torchme/PostFinder?style=flat&labelColor=lightblue&color=1f1f1f.svg) ![GitHub License](https://img.shields.io/github/license/torchme/PostFinder?style=flat&labelColor=lightblue&color=1f1f1f.svg)

<br />

---

## What is it?

**Post Finder** is telegram bot integration semantich search content. 

---
## 1. Installation from sources

#### Requirements

Install required dependencies with the following commands:

```bash
pip install poetry

pip install --upgrade pip

poetry install
```
#### Development

In the development mode install pre-commits with the following commands:

```bash
pre-commit
```

or

```bash
pre-commit install
```

## 2. How to run it?
The first step is to create `.env` file with secret keys or `.env-docker` if you gonna start bot with docker.

*Place for documentation .env*

#### Run the bot

You can run the bot with the following command:

```bash
bash run_bot.sh
```

or with docker:

```bash
docker-compose -f docker/docker-compose.yaml build migrations
docker-compose -f docker/docker-compose.yaml up migrations
```

## Documentation

The official documentation is hosted on [GitBook](https://torchme.gitbook.io/postfinder/)
