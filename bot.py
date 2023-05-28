# from aiogram import executor
import asyncio
from create_bot import dp, bot
from main import event_handler, main_handler, achievement_handler, bdi_test_handler, bai_test_handler, test_choise_handler
from data_base import sql_start



async def on_startup():
    print("...start bot...")
    sql_start()
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


main_handler.register_handlers(dp) 
event_handler.register_handlers_event(dp)
achievement_handler.register_handlers_achievement(dp)
bdi_test_handler.register_handlers_bdi_test(dp)
bai_test_handler.register_handlers_bai_test(dp)
test_choise_handler.regisetr_handlers_test_choise(dp)



if __name__ == '__main__':
    # executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    asyncio.run(on_startup())