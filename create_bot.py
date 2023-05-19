from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage



TOKEN = "5886031842:AAHxo4Fiu6whccdIHFOFor4PMlFUY_ojPzA"

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
