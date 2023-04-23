from aiohttp import ClientSession
from discord.ext import commands, tasks
from typing import Optional
import discord


class Bot(commands.Bot):

    def __init__(
        self,
        *args,
        initial_extensions: list[str],
        web_client: ClientSession,
        testing_guild_id: Optional[int] = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.initial_extensions = initial_extensions
        self.web_client = web_client
        self.testing_guild_id = testing_guild_id

    async def setup_hook(self) -> None:
        self.presence_loop.start()

        for extension in self.initial_extensions:
            await self.load_extension(extension)

        if self.testing_guild_id:
            guild = discord.Object(self.testing_guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        else:
            await self.tree.sync()

    @tasks.loop(minutes=1)
    async def presence_loop(self):
        await self.wait_until_ready()
        await self.change_presence(
            activity=discord.Activity(name=f"{len(self.users)} users",
                                      type=discord.ActivityType.watching))
