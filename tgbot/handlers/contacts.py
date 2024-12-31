from aiogram import types, F, Router, Bot
from tgbot.keyboards.inline import contact_keyboard
from aiogram.types import FSInputFile

contacts_router = Router()

photo = FSInputFile("tgbot/contacts.jpg")
@contacts_router.callback_query(F.data == "contacts")
async def about(callback_query: types.CallbackQuery):
    await callback_query.message.answer_photo(photo=photo, caption="Оберить зв'язок з нами:", reply_markup=contact_keyboard())
    await callback_query.message.edit_reply_markup()
    await callback_query.message.delete()
    await callback_query.answer()


@contacts_router.callback_query(F.data == "phone")
async def phone(callback_query: types.CallbackQuery):
    await callback_query.message.answer_contact(phone_number="Телефон: +380504153340",
                                                first_name="Контактний номер")
    await callback_query.answer()


@contacts_router.callback_query(F.data == "email")
async def email(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Email: sales@unitech-solar.com")
    await callback_query.answer()


@contacts_router.callback_query(F.data == "geo")
async def send_geo(callback_query: types.CallbackQuery, bot: Bot):

    # Указываем геолокацию
    latitude = 46.4845296  # Пример: широта (например, для Нью-Йорка)
    longitude = 30.6633114  # Пример: долгота

    # Отправка геолокации пользователю
    await bot.send_location(
        chat_id=callback_query.from_user.id,
        latitude=latitude,
        longitude=longitude
    )

    await callback_query.answer()
