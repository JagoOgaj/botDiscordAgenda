class SqlQuery:
    @staticmethod
    def query_create_agenda() -> str:
        return """
            INSERT INTO agenda (user_id, matiere, libelle, jour_semaine, date_devoir)
            VALUES (%s, %s, %s, %s ,%s) ;
        """

    @staticmethod
    def query_update_agenda() -> str:
        return """
            UPDATE agenda
            SET matiere = %s, 
                libelle = %s, 
                date_devoir = %s
            WHERE id = %s ;
        """

    @staticmethod
    def query_select_by_date_range() -> str:
        return """
            SELECT * 
            FROM agenda 
            WHERE date_devoir BETWEEN %s AND %s
        """

    @staticmethod
    def query_select_future() -> str:
        return """
            SELECT * 
            FROM agenda
            WHERE date_devoir BETWEEN %s AND %s  -- Utilisation de BETWEEN pour définir une plage
            ORDER BY date_devoir ASC;  -- Ordre croissant par date_devoir
        """

    @staticmethod
    def query_select_all() -> str:
        return """
            SELECT * 
            FROM agenda 
            ORDER BY date_devoir ASC ;
        """

    @staticmethod
    def query_select_one() -> str:
        return """
            SELECT * 
            FROM agenda
            WHERE id = %s ;
    """
