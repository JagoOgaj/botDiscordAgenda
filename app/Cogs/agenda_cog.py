from discord.ext import commands
import discord
from datetime import datetime
import pytz
from app.Managers import db
from app.Models import Agenda
from app.Tools import Static, make_embed_err, make_embed_sucess, command_descriptions
from app.Config import logger


class AgendaCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.db = db

    @commands.command(name="ajouter_devoir")
    async def create(self, ctx: commands.Context, *, params: str):
        try:
            logger.info(
                Static.COMMAND_EXEC.explainedError(command_name=self.create.name)
            )
            params_dict = {}

            params_split = [param.strip() for param in params.split(",")]

            for param in params_split:
                if "=" in param:
                    key_value = param.split("=", 1)
                    key = key_value[0].strip()
                    value = key_value[1].strip().strip('"')
                    params_dict[key] = value

            matiere = params_dict.get("matiere")
            libelle = params_dict.get("libelle")
            date = params_dict.get("date")

            if not matiere or not libelle or not date:
                await ctx.send(
                    embed=make_embed_err(Static.ARG_FORGOTTEN.value).set_thumbnail(
                        url=ctx.guild.icon
                    )
                )
                return

            user_id = ctx.author.id
            date_format = "%d/%m/%Y"
            date_devoir = datetime.strptime(date, date_format)

            paris_tz = pytz.timezone(Static.TIME_ZONE.value)
            date_devoir = paris_tz.localize(date_devoir)

            agenda = Agenda(
                user_id=user_id, matiere=matiere, libelle=libelle, date=date_devoir
            )
            db.create_agenda(agenda)
            await ctx.send(
                embed=make_embed_sucess(Static.DEVOIR_CREER_SUCESS.value).set_thumbnail(
                    url=ctx.guild.icon
                )
            )
            logger.info(Static.COMMAND_EXEC.explained(additional_info=self.create.name))
        except Exception as e:
            await ctx.send(
                embed=make_embed_err(str(e)).set_thumbnail(url=ctx.guild.icon)
            )
            logger.error(
                Static.DESC_ERR.explainedError(
                    command_name=self.create.name, additional_info=str(e)
                )
            )
            raise Exception(
                Static.DESC_ERR.explainedError(
                    command_name=self.create.name, additional_info=str(e)
                )
            ) from e

    @commands.command(name="mise_a_jour")
    async def update(self, ctx: commands.Context, *, updates: str):
        try:
            logger.info(
                Static.COMMAND_EXEC.explainedError(command_name=self.update.name)
            )

            updates_dict = {}
            updates_split = [update.strip() for update in updates.split(",")]

            for update in updates_split:
                if "=" in update:
                    key_value = update.split("=", 1)
                    key = key_value[0].strip()
                    value = key_value[1].strip().strip('"')
                    updates_dict[key] = value

            agenda_id = updates_dict.pop("id", None)

            if agenda_id is None or not updates_dict:
                embed = discord.Embed(
                    title="Erreur 😢",
                    description="Tu dois saisir un ID et au moins un champ à modifier",
                    color=discord.Color.red(),
                )
                embed.set_thumbnail(url=ctx.guild.icon)
                await ctx.send(embed=embed)
                return

            agenda_id = int(agenda_id)

            agenda: None | Agenda = db.get_agenda_by_id(agenda_id)

            if agenda is None:
                raise Exception("Aucun agenda trouvé")
            matiere = updates_dict.get("matiere")
            libelle = updates_dict.get("libelle")
            date = updates_dict.get("date")

            agenda.update_details(matiere, libelle, date)
            db.update_agenda(agenda)

            await ctx.send(
                embed=make_embed_sucess(
                    Static.DEVOIR_UPDATE_SUCESS.value
                ).set_thumbnail(url=ctx.guild.icon)
            )
            logger.info(Static.COMMAND_EXEC.explained(additional_info=self.update.name))

        except Exception as e:
            await ctx.send(
                embed=make_embed_err(str(e)).set_thumbnail(url=ctx.guild.icon)
            )
            logger.error(
                Static.DESC_ERR.explainedError(
                    command_name=self.update.name, additional_info=str(e)
                )
            )
            raise Exception(
                Static.DESC_ERR.explainedError(
                    command_name=self.update.name,
                    additional_info=str(e),
                    sub_info=str(f"id : {agenda_id}"),
                )
            ) from e

    @commands.command(name="tous")
    async def all(self, ctx: commands.Context):
        try:
            logger.info(Static.COMMAND_EXEC.explainedError(command_name=self.all.name))
            agendas = db.get_all_agendas()
            if not agendas:
                embed = discord.Embed(
                    title="Aucun Devoir Trouvé 😢",
                    description="Vous n'avez pas de devoirs à venir. Profitez-en pour vous reposer ou rattraper vos leçons ! 🎉",
                    color=discord.Color.orange(),
                )
                embed.set_thumbnail(url=ctx.guild.icon)
                await ctx.send(embed=embed)
                return

            embed = discord.Embed(
                title="Liste des Devoirs 📚",
                description="Voici tous vos devoirs!",
                color=discord.Color.blue(),
            )

            for agenda in agendas:
                created_by_user = self.bot.get_user(agenda.user_id)

                created_by_name = created_by_user.name if created_by_user else "Inconnu"

                description = (
                    f"**Id : ** {agenda.id_agenda}\n"
                    f"**Libellé :** {agenda.libelle}\n"
                    f"**Date :** {agenda.date.strftime('%d %B %Y')} 🗓️\n"
                    f"**Jour :** {agenda.jour_semaine} 🌞\n"
                    f"**Créé par :** {created_by_name} 👤"
                )

                embed.add_field(
                    name=f"**Matiere : ** {agenda.matiere} 📖",
                    value=description,
                    inline=False,
                )
                embed.add_field(name="\u200b", value="---", inline=False)
            embed.set_footer(text="N'oubliez pas de faire vos devoirs ! 😊")
            embed.set_thumbnail(url=ctx.guild.icon)

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(
                embed=make_embed_err(str(e)).set_thumbnail(url=ctx.guild.icon)
            )
            logger.error(
                Static.DESC_ERR.explainedError(
                    command_name=self.all.name, additional_info=str(e)
                )
            )
            raise Exception(
                Static.DESC_ERR.explainedError(
                    command_name=self.all.name, additional_info=str(e)
                )
            ) from e

    @commands.command(name="devoir_periode")
    async def devoirs_periode(self, ctx: commands.Context, *, params: str):
        try:
            params_dict = {}
            params_split = params.split(",")

            for param in params_split:
                if "=" in param:
                    key_value = param.split("=", 1)
                    key = key_value[0].strip()
                    value = key_value[1].strip()
                    params_dict[key] = value

            start_date = params_dict.get("start")
            end_date = params_dict.get("end")

            if not start_date or not end_date:
                await ctx.send(
                    embed=make_embed_err(Static.ARG_FORGOTTEN.value).set_thumbnail(
                        url=ctx.guild.icon
                    )
                )
                return

            date_format = "%d/%m/%Y"

            start_date_period = datetime.strptime(start_date, date_format)
            end_date_period = datetime.strptime(end_date, date_format)
            paris_tz = pytz.timezone(Static.TIME_ZONE.value)
            start_date_period = paris_tz.localize(start_date_period)
            end_date_period = paris_tz.localize(end_date_period)

            agendas = db.get_agendas_for_period(start_date_period, end_date_period)

            if not agendas:
                embed = discord.Embed(
                    title="Aucun Devoir Trouvé pour cette période 😢",
                    description="Vous n'avez pas de devoirs à venir. Profitez-en pour vous reposer ou rattraper vos leçons ! 🎉",
                    color=discord.Color.orange(),
                )
                embed.set_thumbnail(url=ctx.guild.icon)
                await ctx.send(embed=embed)
                return

            embed = discord.Embed(
                title="Devoirs pour la Période 📅",
                description=f"Voici vos devoirs du {start_date} au {end_date} :",
                color=discord.Color.blue(),
            )

            for agenda in agendas:
                created_by_user = self.bot.get_user(agenda.user_id)

                created_by_name = created_by_user.name if created_by_user else "Inconnu"

                description = (
                    f"**Id : ** {agenda.id_agenda}\n"
                    f"**Libellé :** {agenda.libelle}\n"
                    f"**Date :** {agenda.date.strftime('%d %B %Y')} 🗓️\n"
                    f"**Jour :** {agenda.jour_semaine} 🌞\n"
                    f"**Créé par :** {created_by_name} 👤"
                )

                embed.add_field(
                    name=f"**Matiere : ** {agenda.matiere} 📖",
                    value=description,
                    inline=False,
                )
                embed.add_field(name="\u200b", value="---", inline=False)

            embed.set_footer(text="N'oubliez pas de faire vos devoirs ! 😊")
            embed.set_thumbnail(url=ctx.guild.icon)

            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(
                embed=make_embed_err(str(e)).set_thumbnail(url=ctx.guild.icon)
            )
            logger.error(
                Static.DESC_ERR.explainedError(
                    command_name=self.devoirs_periode.name, additional_info=str(e)
                )
            )
            raise Exception(
                Static.DESC_ERR.explainedError(
                    command_name=self.devoirs_periode.name, additional_info=str(e)
                )
            ) from e

    @commands.command(name="commands", description="Liste toutes les commandes du bot")
    async def list_commands(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Liste des Commandes du Bot 📜",
            description="Voici toutes les commandes disponibles que vous pouvez utiliser :",
            color=discord.Color.green(),
        )

        embed.set_thumbnail(url=ctx.bot.user.avatar.url)

        for command_name, description in command_descriptions.items():
            embed.add_field(
                name=f"{self.bot.command_prefix}{command_name}",
                value=description,
                inline=False,
            )

        embed.add_field(
            name="🔗 GitHub",
            value="[Cliquez ici pour accéder au dépôt GitHub](https://github.com/JagoOgaj/botDiscordAgenda)",
            inline=False,
        )
        embed.set_footer(text="Utilisez chaque commande avec prudence ! 😊")
        await ctx.send(embed=embed)
