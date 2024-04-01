from ruamel.yaml import YAML
from loguru import logger


class Config:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.yaml = YAML()
        self.yaml.preserve_quotes = True
        self.yaml.indent(mapping=2, sequence=4, offset=2)
        self.admin_ids = []
        self.whitelist = []
        self.load_ids()
        logger.info(f"Config initialized with {self.filename}")

    def load_ids(self):
        """Load user and admin IDs from the configuration file into attributes."""
        config = self._load_config()
        self.admin_ids = config.get("admins", [])
        self.whitelist = config.get("users", [])
        logger.info("Admin and user IDs loaded from config.")

    def add_id(self, id_type, user_id):
        """
        Add a unique user or admin ID to the respective list in the configuration and update the attribute.

        Parameters
        ----------
        id_type : str
            The type of ID to add ('admins' or 'users').
        user_id : int
            The ID of the user or admin to add.

        Returns
        -------
        bool
            True if the ID was added, False if the ID was already present.
        """
        config = self._load_config()

        if config.get(id_type) is None:
            config[id_type] = []

        if user_id not in config[id_type]:
            config[id_type].append(user_id)
            self._save_config(config)

            if id_type == "users":
                self.whitelist.append(user_id)
            elif id_type == "admins":
                self.admin_ids.append(user_id)

            logger.info(f"ID {user_id} added to the {id_type} list and saved.")
            return True
        else:
            logger.warning(f"ID {user_id} is already in the {id_type} list.")
            return False

    def remove_id(self, id_type, user_id):
        """
        Remove a user or admin ID from the respective list in the configuration and update the attribute.


        Parameters
        ----------
        id_type : str
            The type of ID to remove ('admins' or 'users').
        user_id : int
            The ID of the user or admin to remove.

        Returns
        -------
        bool
            True if the ID was removed, False if the ID was not found.
        """
        config = self._load_config()

        if config.get(id_type) and user_id in config[id_type]:
            config[id_type].remove(user_id)
            self._save_config(config)

            if id_type == "users":
                self.whitelist.remove(user_id)
            elif id_type == "admins":
                self.admin_ids.remove(user_id)

            logger.info(f"ID {user_id} removed from the {id_type} list and saved.")
            return True
        else:
            logger.error(f"ID {user_id} not found in the {id_type} list.")
            return False

    def get(self, keys: list)  -> str:
        """
        Get value from config.
        Parameters
        ----------
        keys: list
            List of strings(keys for yaml)  ('admins' or 'users').
        Returns
        -------
        int or str
            Value from yaml config.
        """
        config = self._load_config()
        value = config
        pointer = 0
        try:
            while pointer!=len(keys):
                value = value[keys[pointer]]
                pointer += 1
            return value
        
        except Exception:
            # logger.error(f"Failed to get value by keys {keys}")
            print(f"Failed to get value by keys {keys}")
    def _load_config(self) -> dict:
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                return self.yaml.load(file) or {}
        except FileNotFoundError as e:
            logger.error(f"Configuration file not found: {e}")
            return {}

    def _save_config(self, config: dict) -> None:
        try:
            with open(self.filename, "w", encoding="utf-8") as file:
                self.yaml.dump(config, file)
            logger.info(f"Configuration saved to {self.filename}")
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")

