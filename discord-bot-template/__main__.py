import asyncio
import os

import discord.utils
from aiohttp import ClientSession
from discord.ext import commands
from dotenv import load_dotenv

from classes.bot import Bot


async def main():
    discord.utils.setup_logging()

    async with ClientSession() as web_client:
        extensions = []
        intents = discord.Intents.default()
        async with Bot(
                commands.when_mentioned,
                intents=intents,
                web_client=web_client,
                initial_extensions=extensions,
        ) as bot:
            await bot.start(os.getenv("TOKEN"))


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
