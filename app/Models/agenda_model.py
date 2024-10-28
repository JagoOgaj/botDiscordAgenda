from datetime import datetime
from app.Config import logger
from app.Tools import Static, jours_francais
from app.Utils import validate_agenda_attributes
import pytz


@validate_agenda_attributes
class Agenda:
    def __init__(self, user_id: int, matiere: str, libelle: str, date: datetime):
        self._id: int | None = None
        self._user_id: int = user_id
        self._matiere: str = matiere
        self._libelle: str = libelle
        self._date: datetime = date
        self._jour = jours_francais[date.strftime("%A")]

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def matiere(self) -> str:
        return self._matiere

    @property
    def libelle(self) -> str:
        return self._libelle

    @property
    def date(self) -> datetime:
        return self._date

    @property
    def id_agenda(self) -> int:
        if id := (self._id):
            return id

    @id_agenda.setter
    def id_agenda(self, value) -> None:
        self._id = value

    @property
    def jour_semaine(self) -> str:
        return self._jour

    def is_time_lef(self) -> bool:
        paris_tz = pytz.timezone(Static.TIME_ZONE.value)
        current_date = datetime.now(paris_tz).date()
        return current_date < self._date

    def update_details(
        self,
        matiere: str | None = None,
        libelleParm: str | None = None,
        date_devoir: str | None = None,
    ):
        try:
            if matiere is not None:
                self._matiere = matiere
            if libelleParm is not None:
                self._libelle = libelleParm
            if date_devoir is not None:
                date_format = "%d/%m/%Y"
                date_devoir = datetime.strptime(date_devoir, date_format)
                paris_tz = pytz.timezone(Static.TIME_ZONE.value)
                date_devoir = paris_tz.localize(date_devoir)
                self._date = date_devoir
                self._jour = jours_francais[date_devoir.strftime("%A")]

        except Exception as e:
            raise Exception(str(e))

    def __str__(self) -> str:
        return f"Module : {self._matiere} - Libelle : {self._libelle} - Date : {self._date}"
