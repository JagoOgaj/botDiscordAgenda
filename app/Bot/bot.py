import discord
from discord.ext import commands
from app.Tools import Static, make_embed_err
from app.Config import logger
from app.Cogs import AgendaCog
from discord.ext import tasks

type botType = BotAgenda

class BotAgenda(commands.Bot):
    
    def __init__(self : botType) -> None :
        super().__init__(command_prefix="!", intents=discord.Intents.all())
        
    async def setup_hook(self : botType):
        logger.info(Static.SYNC.value)
        await self.add_cog(AgendaCog(self))
        commands = await self.tree.sync()
       
    
    async def on_ready(self : botType) -> None:
        logger.info(Static.BOT_START.value)
        game = discord.Streaming(name="Timeless", url="https://www.youtube.com/watch?v=E9fxFF9rbeM")
        await self.change_presence(status=discord.Status.idle, activity=game)
    
    async def on_command_error(self : botType, ctx: commands.Context, error: Exception) -> None :
        logger.error(Static.LOG_ERROR.explainedError(command_name=ctx.command, additional_info=error))
        desc: str = Static.DESC_ERR.explainedError(command_name=ctx.command, additional_info=error)
        if isinstance(error, commands.CommandNotFound):
            desc = Static.COMMAND_NOT_FOUND.explainedError(command_name=ctx.command, additional_info=error)
        elif isinstance(error, commands.MissingRequiredArgument):
            desc = Static.ARG_FORGOTTEN.explainedError(command_name=ctx.command, sub_info=error.param)
        
        await ctx.send(embed=make_embed_err(desc).set_thumbnail(url=ctx.guild.icon))
