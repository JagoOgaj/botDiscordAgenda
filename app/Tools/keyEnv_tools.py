from enum import Enum as e


class KeyEnv(e):
    DISCORD_TOKEN: str = "DISCORD_TOKEN"
    DB_NAME: str = "DB_NAME"
    DB_HOST: str = "DB_HOST"
    DB_USER: str = "DB_USER"
    DB_PWD: str = "DB_PWD"
    LOG_LEVEL: str = "LOG_LEVEL"
