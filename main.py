from aiogram import executor
from bot.loader import dp
from bot.handlers import commands  # , callbacks, messages


commands.register_handlers(dispatcher=dp)
# message.register_handlers(dispatcher=dp)
# callback_query.register_handlers(dispatcher=dp)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True)
