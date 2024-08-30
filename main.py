import os
import logging
import config
import asyncio
from config import COMMANDS_FOLDER
from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

import discord
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
logger = logging.getLogger(__name__)


# Init bot
intents = discord.Intents.default()
intents.message_content = True
loop = asyncio.get_event_loop()
bot = discord.Bot(intents=intents, loop=loop)


@bot.event
async def on_ready():
    print(f"{bot.user} is running !")

for filepath in COMMANDS_FOLDER.rglob('*.py'):
    relative_path = filepath.relative_to(COMMANDS_FOLDER).with_suffix('')
    module_name = f"commands.{relative_path.as_posix().replace('/', '.')}"

    logging.info(f'Loading {module_name}')
    bot.load_extension(module_name)

app = FastAPI()
config = uvicorn.Config(app, loop="asyncio")
server = uvicorn.Server(config)

@app.get("/")
async def ping():
    return {"message": "pong"}

async def start() -> None:
    await asyncio.gather(bot.start(BOT_TOKEN), server.serve())

try:
    loop.run_until_complete(start())
finally:
    if not bot.is_closed():
        loop.run_until_complete(bot.close())
    if server.started:
        loop.run_until_complete(server.shutdown())
