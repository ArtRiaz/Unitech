from aiogram import Router, types, Bot, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from tgbot.keyboards.inline import start_keyboard_user
from aiogram.utils.deep_linking import create_start_link
from infrastructure.database.repo.request import RequestsRepo
from aiogram.types import FSInputFile

user_router = Router()

photo = FSInputFile("tgbot/logoo.jpeg")

caption = ("- Приглашаем в команду корабелов. Информация о вакансиях.\n- Требуются:\nСборщики металлических "
           "конструкций судов, сварщики ,трубопроводчики судовые,сварщики по трубам\n\nЧтоб подробнее узнать о нашей "
           "компании нажмите раздел о нас\nЕсли вы желаете подать заяку на вакансию нажмите раздел регистрация")


@user_router.message(CommandStart())
async def start(message: Message, bot: Bot, command: CommandObject, repo: RequestsRepo):
    await message.answer_photo(photo=photo,
                               caption=f"Привет {message.from_user.username}\n{caption}"
                               ,
                               reply_markup=start_keyboard_user())


@user_router.callback_query(F.data == "back")
async def about(callback_query: types.CallbackQuery):
    await callback_query.message.answer_photo(photo=photo,
                                              caption=f"{caption}",
                                              reply_markup=start_keyboard_user())
    await callback_query.message.edit_reply_markup()
    await callback_query.answer()
