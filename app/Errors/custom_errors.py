class DatabaseConnectionErrors(Exception):
    def __init__(self, details: str | None = None):
        super().__init__(f"Erreur de connexion. {'\n Details : ' + details if details else ''}")
        self.details : str | None = details
        
        
class DataBaseCloseErrors(Exception):
    def __init__(self, details: str | None = None):
        super().__init__(f"Erreur lors de la fermeture de la connexion à la base de données. {'\n Details : ' + details if details else ''}")
        self.details : str | None = details
        
        
class NullField(Exception):
    def __init__(self, message: str):
        if not message:
            raise ValueError("Not null message")
        
        super().__init__(message)
        self.message: str = message
        
        
class WrongTypeField(Exception):
    def __init__(self, message : str):
        if not message :
            raise ValueError("Not null message")
        super().__init__(message)
        self.message: str = message