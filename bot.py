from aiogram import executor
from create_bot import dp, bot
from main import event_handler, main_handler, achievement_handler, bdi_test_handler, bai_test_handler, test_choise_handler
from data_base import sql_start
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from main import scheduled
from datetime import datetime, timedelta


async def on_startup(_):
    print("...start bot...")
    sql_start()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(scheduled.achievement_reminder, trigger='cron', hour=19, minute=0)
    scheduler.add_job(scheduled.event_reminder, trigger='cron', hour=20, minute=0)
    scheduler.add_job(scheduled.bdi_test_reminder, trigger='cron', day_of_week='mon', hour=19, minute=30)
    scheduler.add_job(scheduled.bai_test_reminder, trigger='cron', day_of_week='fri', hour=19, minute=30)
    scheduler.start()



main_handler.register_handlers(dp) 
event_handler.register_handlers_event(dp)
achievement_handler.register_handlers_achievement(dp)
bdi_test_handler.register_handlers_bdi_test(dp)
bai_test_handler.register_handlers_bai_test(dp)
test_choise_handler.regisetr_handlers_test_choise(dp)
scheduled.register_handlers_reminder(dp)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    # asyncio.run(on_startup())