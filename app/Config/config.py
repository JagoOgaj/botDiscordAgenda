import os
import logging
from dotenv import load_dotenv
from app.Tools import (
    KeyEnv,
    Static,
)
load_dotenv(override=True)
type configType = Config

class Config:
    _instance: configType | None = None
    
    def __new__(cls: configType | None) -> None | configType :
        if cls._instance is None :
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self : configType) -> None:
        self._discordBotToken: str = os.getenv(KeyEnv.DISCORD_TOKEN.value)
        self._dbUser: str = os.getenv(KeyEnv.DB_USER.value)
        self._dbPwd: str = os.getenv(KeyEnv.DB_PWD.value)
        self._dbHost: str = os.getenv(KeyEnv.DB_HOST.value)
        self._dbName: str = os.getenv(KeyEnv.DB_NAME.value)
        self._dbConfigObject: dict[str, str] = self.getDbConfig()
        self._logLevel: str = os.getenv(KeyEnv.LOG_LEVEL.value, Static.LOG_LEVEL.value)
        self._logger : logging.Logger = self.setup_logger()
        
    
    @property
    def dicordBotToken(self : configType) -> str:
        return self._discordBotToken
    
    @property
    def db_user(self : configType) -> str:
        return self._dbUser
    
    @property
    def db_pwd(self : configType) -> str:
        return self._dbPwd
    
    @property
    def db_host(self : configType) -> str:
        return self._dbHost
    
    @property
    def db_name(self : configType) -> str:
        return self._dbName
    
    @property
    def log_level(self : configType) -> str:
        return self._logLevel
    
    @property
    def logger(self : configType) -> logging.Logger :
        return self._logger
    
    def getDbConfig(self) -> dict[str, str]:
         return {
            'host': self._dbHost,
            'user': self._dbUser,
            'password': self._dbPwd,
            'database': self._dbName
        }
    
    def setup_logger(self : configType) -> logging.Logger :
        log_level = getattr(logging, self.log_level.upper(), logging.INFO)
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
            logging.StreamHandler() 
            ]
        )
        logger = logging.getLogger(__name__)
        logger.setLevel(log_level)
        return logger
        
config : configType = Config()
logger : logging.Logger = config.logger

