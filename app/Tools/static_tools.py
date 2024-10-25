from enum import Enum as e
import discord
import datetime


class Static(e):
    LOG_LEVEL: str = "INFO"
    BOT_START: str = "Le bot est lancé"
    LOG_ERROR: str = "Une erreur est survenue"
    TITLE_SUCESS: str = "Succes"
    DESC_SUCESS: str = "Commande a fonctionne"
    TITLE_ERR: str = "Erreur"
    DESC_ERR: str = "Une erreur est survenue"
    COMMAND_NOT_FOUND: str = "Commande non trouvée."
    ARG_FORGOTTEN: str = "Argument manquant"
    DB_CONNECTED: str = "Connexion a la base de donnee reussie"
    DB_CONN_ERR: str = "Erreur de connexion à la base de données"
    DB_CLOSE_ERR: str = "Une erreur est survenue lors de la fermeture de la session"
    DB_CLOSE_SUCESS: str = "Connexion à la base de données fermée."
    FIELD_NULL: str = "Ce champs ne dois pas etre null"
    FIELD_WRONG_TYPE: str = "Ce champs est du mauvais type"
    TIME_ZONE: str = "Europe/Paris"
    EXEC_QUERY: str = "Excecution de la requete"
    EXEC_QUERY_SUCESS: str = "Requête exécutée avec succès."
    EXEC_QUERY_COMMIT_SUCESS: str = "Requête exécutée et modifications sauvegardées."
    EXEC_QUERY_ERR: str = "Erreur d'exécution de la requête SQL"
    DEVOIR_CREER_SUCESS: str = "Devoir creer avec sucess"
    COOLDOWN_ERROR: str = "Retry dans"
    UNKNOW_AGENDA: str = "Aucun agenda trouver"
    DEVOIR_UPDATE_SUCESS: str = "Devoir mis a jour avec sucess"
    COMMAND_EXEC: str = "Commande executer"
    SYNC: str = "Sync called"

    def explainedError(
        self,
        command_name: str | None = None,
        additional_info: str | None = None,
        sub_info: str | None = None,
    ) -> str:
        return (
            f"{self.value} "
            f"{'pour la commande ' + '***'+str(command_name)+'***'  if command_name else ''} "
            f"{'-> Desc : ' + str(additional_info) if additional_info else ''} "
            f"{str(sub_info) if sub_info else ''}"
        )

    def explained(
        self, additional_info: str | None = None, sub_info: str | None = None
    ) -> str:
        return (
            f"{self.value} "
            f"{'-> Desc : ' + additional_info if additional_info else ''} "
            f"{sub_info if sub_info else ''}"
        )


def make_embed_err(desc: str | None = None) -> discord.Embed:
    return discord.Embed(
        title=Static.TITLE_ERR.value,
        description=desc if desc else Static.DESC_ERR.value,
        color=discord.Color.red(),
        timestamp=datetime.datetime.now(),
    )


def make_embed_sucess(desc: str | None = None) -> discord.Embed:
    return discord.Embed(
        title=Static.TITLE_SUCESS.value,
        description=desc if desc else Static.DESC_SUCESS.value,
        color=discord.Color.green(),
        timestamp=datetime.datetime.now(),
    )


jours_francais: dict[str, str] = {
    "Monday": "Lundi",
    "Tuesday": "Mardi",
    "Wednesday": "Mercredi",
    "Thursday": "Jeudi",
    "Friday": "Vendredi",
    "Saturday": "Samedi",
    "Sunday": "Dimanche",
}

command_descriptions: dict[str, str] = {
    "ajouter_devoir": (
        "Cette commande permet de créer un devoir.\n"
        "**Paramètres :**\n"
        "- `matiere` (obligatoire) : La matière du devoir.\n"
        "- `libelle` (obligatoire) : Le libellé du devoir.\n"
        "- `date` (obligatoire) : La date d'échéance du devoir au format 'j/m/y' (ex : 27/12/2004).\n"
        '**Exemple :** `!ajouter_devoir matiere="Test Du Medzik", libelle="Turfu", date=27/12/2004`'
    ),
    "mise_a_jour": (
        "Mettre à jour les informations d'un devoir.\n"
        "**Paramètres :**\n"
        "- `id` (obligatoire) : L'ID du devoir à mettre à jour.\n"
        "- `matiere` (optionnel) : La nouvelle matière du devoir.\n"
        "- `libelle` (optionnel) : Le nouveau libellé du devoir.\n"
        "- `date` (optionnel) : La nouvelle date d'échéance du devoir au format 'j/m/y'.\n"
        '**Exemple :** `!mise_a_jour id=1, matiere="Mathématiques", libelle="Devoir d\'algèbre"`'
    ),
    "tous": (
        "Liste tous les devoirs enregistrés en base de données.\n"
        "**Paramètres :**\n"
        "- Aucun\n"
        "**Exemple :** `!tous`"
    ),
    "devoir_periode": (
        "Récupérer les devoirs d'une période donnée.\n"
        "**Paramètres :**\n"
        "- `start` (obligatoire) : La date de début au format 'j/m/y' (ex : 27/12/2004).\n"
        "- `end` (obligatoire) : La date de fin au format 'j/m/y' (ex : 27/12/2004).\n"
        "**Exemple :** `!devoir_periode start=27/12/2004, end=22/01/2024`"
    ),
}
