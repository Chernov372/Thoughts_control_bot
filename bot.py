from aiogram import executor
from create_bot import dp, bot
from main import event_handler, main_handler, achievement_handler, bdi_test_handler, bai_test_handler, test_choise_handler
from data_base import sql_start
# from create_bot import bot
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from main import scheduled
# from datetime import datetime


async def on_startup(_):
    print("...start bot...")
    sql_start()
    # scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    # scheduler.add_job(scheduled.event_reminder, trigger='cron', hour=datetime.now().hour, minute=datetime.now().minute+1, start_date=datetime.now(), kwargs={'bot': bot})
    # scheduler.start()


main_handler.register_handlers(dp) 
event_handler.register_handlers_event(dp)
achievement_handler.register_handlers_achievement(dp)
bdi_test_handler.register_handlers_bdi_test(dp)
bai_test_handler.register_handlers_bai_test(dp)
test_choise_handler.regisetr_handlers_test_choise(dp)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
