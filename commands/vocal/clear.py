import discord
from discord.ext import commands
from bot.vocal import ServerSession, server_sessions


class Clear(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.slash_command(
        name='clear',
        description='Clear the queue and stop the current song.'
    )
    async def clear(self, ctx: discord.ApplicationContext) -> None:
        guild_id = ctx.guild.id
        session: ServerSession | None = server_sessions.get(guild_id)

        if session:
            voice_client = session.voice_client
            session.queue.clear()
            session.to_loop.clear()

            if voice_client.is_playing():
                voice_client.stop()

            await ctx.respond('Queue cleared!')


def setup(bot):
    bot.add_cog(Clear(bot))
