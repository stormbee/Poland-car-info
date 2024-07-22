import asyncio
import user_handlers
from os import getenv
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommandScopeDefault, BotCommand
async def main():
    
    bot = Bot(token=getenv("TOKEN"), default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()
    dp.include_router(user_handlers.router)
    await bot.set_my_commands(commands=[
        BotCommand(command="/start", description="Start the bot"),
        ], 
                              scope=BotCommandScopeDefault())
    await bot.get_updates(offset=-1)
    await dp.start_polling(bot)
    
    
if __name__ == "__main__":
    asyncio.run(main())