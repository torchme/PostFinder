from src.config import config

# config = config._load_config()
print(config.get(['messages', 'admin', 'add', 'success']).format(82))