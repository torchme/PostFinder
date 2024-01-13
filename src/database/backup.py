import subprocess
import datetime
from loguru import logger

from src.config import DB_HOST, DB_NAME, DB_PORT, DB_USER


def backup_database(
    backup_path: str = "src/artifacts",
    host: str = DB_HOST,
    port: str = DB_PORT,
    user: str = DB_USER,
    dbname: str = DB_NAME,
):
    date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{backup_path}/backup_{dbname}_{date_str}.dump"

    command = f"pg_dump -h {host} -p {port} -U {user} -d {dbname} -F c > {filename}"

    try:
        subprocess.run(command, check=True, shell=True)
        logger.debug(f"Backup successful: {filename}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error during backup: {e}")


def restore_database(
    backup_filepath: str,
    host: str = DB_HOST,
    port: str = DB_PORT,
    user: str = DB_USER,
    dbname: str = DB_NAME,
):
    command = (
        f"pg_restore -h {host} -p {port} -U {user} -d {dbname} < {backup_filepath}"
    )

    try:
        subprocess.run(command, shell=True)
        logger.debug(f"Database restored successfully from {backup_filepath}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error during database restore: {e}")
