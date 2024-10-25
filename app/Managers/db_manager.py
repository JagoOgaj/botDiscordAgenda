import mysql.connector as MS
from mysql.connector import Error
from datetime import datetime
from app.Config import config, logger
from app.Errors import DataBaseCloseErrors, DatabaseConnectionErrors
from app.Tools import Static, SqlQuery
from app.Models import Agenda

type dbType = DatabaseManager

class DatabaseManager:
    _instance: dbType | None = None
   
    def __new__(cls: dbType | None) -> None | dbType:
        
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self : dbType) -> None:
        try :
            self.conn = MS.connect(**config.getDbConfig())
            if self.conn.is_connected() :
                logger.info(Static.DB_CONNECTED.value)
                self.cursor = self.conn.cursor()
        except Error as e:
            logger.error(Static.DB_CONN_ERR.explainedError(additional_info=str(e)))
            self.connection = None
            self.cursor = None
            raise DatabaseConnectionErrors(str(e)) from e
            
    def execute_query(self, query: str, params: tuple = (), fetch: bool = False):
        try:
            if not self.conn or not self.conn.is_connected():
                raise DatabaseConnectionErrors(Static.DB_CONN_ERR.value)
            
            logger.info(Static.EXEC_QUERY.explained(additional_info=query, sub_info=str(params)))
            self.cursor.execute(query, params)
            
            if fetch:
                result = self.cursor.fetchall()
                logger.info(Static.EXEC_QUERY_SUCESS.explained(additional_info=query, sub_info=str(params)))
                return result
            
            self.conn.commit()
            logger.info(Static.EXEC_QUERY_COMMIT_SUCESS.value)
            
        except (Error, Exception) as e :
            logger.error(Static.EXEC_QUERY_ERR.explainedError(additional_info=str(e)))
            self.conn.rollback()
            raise Exception(f"Erreur d'exécution de la requête SQL : {str(e)}") from e

    def create_agenda(self, agenda: Agenda):
        query = SqlQuery.query_create_agenda()
        params = (agenda.user_id, agenda.matiere, agenda.libelle, agenda.jour_semaine ,agenda.date)
        try:
            self.execute_query(query, params)
            logger.info(Static.EXEC_QUERY_SUCESS.explained(additional_info=query, sub_info=str(params)))
        except (Error, Exception) as e :
            logger.error(Static.EXEC_QUERY_ERR.explainedError(additional_info=str(e)))
            raise Exception(f"Erreur d'exécution de la requête SQL : {str(e)}") from e
    
    def update_agenda(self, agenda: Agenda):
        query = SqlQuery.query_update_agenda()
        params = (agenda.matiere, agenda.libelle, agenda.date, agenda.id_agenda)
        try:
            self.execute_query(query, params)
            logger.info(Static.EXEC_QUERY_SUCESS.explained(additional_info=query, sub_info=str(params)))
        except (Error, Exception) as e :
            logger.error(Static.EXEC_QUERY_ERR.explainedError(additional_info=str(e)))
            raise Exception(f"Erreur d'exécution de la requête SQL : {str(e)}") from e

    def get_agendas_for_period(self, start_date: str, end_date: str) -> list:
        query = SqlQuery.query_select_by_date_range()
        params = (start_date, end_date)
        try:
            result = self.execute_query(query, params, fetch=True)
            return [self._convert_to_agenda(row) for row in result]
        except (Error, Exception) as e :
            logger.error(Static.EXEC_QUERY_ERR.explainedError(additional_info=str(e)))
            return []

    def get_future_agendas(self, current_date) -> list:
        query = SqlQuery.query_select_future()
        params = (current_date,)
        
        try:
            result = self.execute_query(query, params, fetch=True)
            return [self._convert_to_agenda(row) for row in result]
        except (Error, Exception) as e :
            logger.error(Static.EXEC_QUERY_ERR.explainedError(additional_info=str(e)))
            return []
        
    def get_agenda_by_id(self, agenda_id: int) -> Agenda | None:
        query = SqlQuery.query_select_one()
        params = (agenda_id,)
        
        try:
            result = self.execute_query(query, params, fetch=True)
            if result:
                return self._convert_to_agenda(result[0]) 
            else:
                logger.warning(Static.UNKNOW_AGENDA.explainedError(additional_info=agenda_id))
                return None
        except (Error, Exception) as e :
            logger.error(Static.EXEC_QUERY_ERR.explainedError(additional_info=str(e)))
            return None
    
    def get_all_agendas(self) -> list:
        query = SqlQuery.query_select_all()
        try:
            result = self.execute_query(query, fetch=True)
            agendas = []
            for row in result:

                agendas.append(self._convert_to_agenda(row))
            return agendas
        except Exception as e:
            logger.error(Static.EXEC_QUERY_ERR.explainedError(additional_info=str(e)))
            return []
    
    def close(self):
        try :
            if self.cursor:
                self.cursor.close()
            if self.connection and self.connection.is_connected():
                self.connection.close()
                logger.info(Static.DB_CLOSE_SUCESS.value)
                self.connection = None 
        except (Error, Exception) as e :
            logger.error(Static.DB_CLOSE_ERR.explainedError(additional_info=str(e)))
            raise DataBaseCloseErrors(str(e)) from e
        
    def _convert_to_agenda(self, row) -> Agenda:
        agenda = Agenda(
            user_id=row[1], 
            matiere=row[2], 
            libelle=row[3], 
            date=row[5]     
        )
        agenda.id_agenda = row[0] 
        return agenda
    
    
db : dbType = DatabaseManager()