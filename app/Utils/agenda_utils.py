from app.Config import logger
from app.Errors import NullField, WrongTypeField
from app.Tools import Static
from functools import wraps


def validate_agenda_attributes(cls):
    original_init = cls.__init__

    def new_init(self, user_id, matiere, libelle, date):
        if not user_id:
            err: str = Static.FIELD_NULL.explainedError(additional_info="user_id")
            logger.error(err)
            raise NullField(err)

        if not isinstance(user_id, int):
            err: str = Static.FIELD_WRONG_TYPE.explainedError(additional_info="user_id")
            logger.error(err)
            raise WrongTypeField(err)

        if not matiere:
            err: str = Static.FIELD_NULL.explainedError(additional_info="matiere")
            logger.error(err)
            raise NullField(err)

        if not isinstance(matiere, str):
            err: str = Static.FIELD_WRONG_TYPE.explainedError(additional_info="matiere")
            logger.error(err)
            raise WrongTypeField(err)

        if not libelle:
            err: str = Static.FIELD_NULL.explainedError(additional_info="libelle")
            logger.error(err)
            raise NullField(err)

        if not isinstance(libelle, str):
            err: str = Static.FIELD_WRONG_TYPE.explainedError(additional_info="libelle")
            logger.error(err)
            raise WrongTypeField(err)

        logger.info(
            f"Création d'une instance de {cls.__name__} avec user_id: {user_id}, matiere: {matiere}, libelle: {libelle}, date : {date}"
        )
        original_init(self, user_id, matiere, libelle, date)

    cls.__init__ = new_init
    return cls
