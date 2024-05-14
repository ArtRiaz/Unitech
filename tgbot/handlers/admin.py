from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from tgbot.keyboards.inline import admin_kb, back_admin
from aiogram.types import FSInputFile
from tgbot.filters.admin import AdminFilter
from infrastructure.database.repo.request import RequestsRepo
import logging

admin_router = Router()
admin_router.message.filter(AdminFilter())

caption = ("Желаю удачного полета 🕊\n\n"
           "Тихо, тихо ползи,\n"
           "Улитка, по склону Фудзи\n"
           "Вверх, до самых высот!")


@admin_router.message(CommandStart())
async def admin_start(message: Message):
    await message.answer_photo(photo=FSInputFile("tgbot/admin.png"),
                               caption=f"{caption}", reply_markup=admin_kb())


@admin_router.callback_query(F.data == "view_requests")
async def view_requests(callback_query: types.CallbackQuery, repo: RequestsRepo):
    try:
        result = await repo.select.select_all_registers()
        formatted_result = '\n\n'.join([f"Имя: {r.name} Возраст: {r.age}"
                                        f" Опыт: {r.expirience}"
                                        f" Специальность: {r.profession}"
                                        f" Контакт: {r.contact}" for r in result])

        await callback_query.message.answer(f"Все заявки:\n"
                                            f"{formatted_result}", reply_markup=back_admin())
    except Exception as e:
        await callback_query.message.answer(f'Произошла ошибка при получении заявок.{e}', reply_markup=back_admin())
    finally:
        await callback_query.answer()


@admin_router.callback_query(F.data == "view_users")
async def view_users(callback_query: types.CallbackQuery, repo: RequestsRepo):
    try:
        result = await repo.count_users.count_users()
        res = len(result)
        await callback_query.message.answer(f"Количество пользователей: {res}", reply_markup=back_admin())
    except Exception as e:
        await callback_query.message.answer(f'Произошла ошибка при получении пользователей.{e}', reply_markup=back_admin())
    finally:
        await callback_query.answer()


@admin_router.callback_query(F.data == "back_admin")
async def back(callback_query: types.CallbackQuery):
    await callback_query.message.answer_photo(photo=FSInputFile("tgbot/admin.png"),
                                              caption=f"{caption}", reply_markup=admin_kb())
    await callback_query.message.edit_reply_markup()
    await callback_query.answer()
