from aiogram import types, F, Router
from tgbot.keyboards.inline import contact_keyboard

contacts_router = Router()


@contacts_router.callback_query(F.data == "contacts")
async def about(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Выберете связь с нами:", reply_markup=contact_keyboard())
    await callback_query.answer()


@contacts_router.callback_query(F.data == "phone")
async def phone(callback_query: types.CallbackQuery):
    await callback_query.message.answer_contact(phone_number="Телефон: +37067074030",
                                                first_name="Контактный номер")
    await callback_query.answer()


@contacts_router.callback_query(F.data == "email")
async def email(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Email: litsomahr@gmail.com")
    await callback_query.answer()
