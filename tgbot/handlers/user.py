import logging

from aiogram import Router, types, Bot, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery
from tgbot.keyboards.inline import start_keyboard_user
from aiogram.utils.deep_linking import create_start_link
from infrastructure.database.repo.request import RequestsRepo
from aiogram.types import FSInputFile
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import FSInputFile
import os
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command

user_router = Router()

photo = FSInputFile("tgbot/Main-Pic.jpg")

caption = ("Unitech Solar — Інженерні рішення для сонячної енергетики\n"
           "під будь-які завдання\n"
           "Ми не просто продаємо обладнання — ми створюємо ефективні системи для вашого бізнесу")


@user_router.message(CommandStart())
@user_router.callback_query(F.data == 'start')
async def start(event: Message | CallbackQuery, bot: Bot, repo: RequestsRepo):
    # Определяем тип события
    if isinstance(event, Message):
        user_name = event.from_user.username or "гость"
        await event.answer_photo(
            photo=photo,
            caption=f"Привет, {user_name}!\n{caption}",
            reply_markup=start_keyboard_user()
        )

    elif isinstance(event, CallbackQuery):
        user_name = event.from_user.username or "гость"
        await bot.send_photo(
            chat_id=event.message.chat.id,
            photo=photo,
            caption=f"Привет, {user_name}!\n{caption}",
            reply_markup=start_keyboard_user()
        )
        await bot.answer_callback_query(event.id)


@user_router.callback_query(F.data == "back")
async def about(callback_query: types.CallbackQuery):
    await callback_query.message.answer_photo(photo=photo,
                                              caption=f"{caption}",
                                              reply_markup=start_keyboard_user())
    await callback_query.message.edit_reply_markup()
    await callback_query.message.delete()
    await callback_query.answer()


@user_router.callback_query(F.data == "online")
async def online(callback_query: types.CallbackQuery, bot: Bot):
    user_name = callback_query.from_user.username
    keyboards = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Вiдповiсти клiєнту", url=f"https://t.me/{user_name}")]
        ]
    )
    await bot.send_message(chat_id=-1002185862798,
                           text="📞 Виклик оператора",
                           reply_markup=keyboards)


@user_router.message(F.text == "Админ")
async def get_admin_menu(message: types.Message, bot: Bot):
    keyboards = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="База Данних", callback_data="database")],
            [InlineKeyboardButton(text="Розсилання", callback_data="send")]
        ]
    )
    await message.bot.send_message(chat_id=-1002185862798, text="Меню Адмiнiстратора", reply_markup=keyboards)


@user_router.callback_query(F.data == "database")
async def get_database(callback: types.CallbackQuery, repo: RequestsRepo):
    """
    Обработчик кнопки "База Данних". Сохраняет всех пользователей (user_id и username) в txt-файл и отправляет его.
    """
    try:
        # Получаем пользователей через репозиторий
        users = await repo.count_users.count_users()

        # Проверяем, есть ли пользователи
        if not users:
            await callback.message.answer("База даних порожня.")
            return

        # Формируем список пользователей
        user_list = "\n".join([f"{user_id} - {username or 'No username'}" for user_id, username in users])

        # Сохраняем список в текстовый файл
        file_path = "users_database.txt"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("Список користувачів бази даних:\n\n")
            file.write(user_list)

        # Отправляем файл пользователю
        file_to_send = FSInputFile(file_path)
        await callback.message.answer_document(file_to_send, caption="Список користувачів бази даних.")

    except Exception as e:
        # Логируем ошибку и уведомляем пользователя
        logging.error(f"Ошибка при получении данных из базы: {e}")
        await callback.message.answer("Сталася помилка під час отримання даних із бази. Спробуйте пізніше.")

    finally:
        # Удаляем файл после отправки
        if os.path.exists(file_path):
            os.remove(file_path)


@user_router.callback_query(F.data == "send")
async def broadcast_message(callback: types.CallbackQuery, state: FSMContext):
    """
    Обработчик кнопки "Розсилання". Запрашивает текст для рассылки.
    """
    await state.set_state("broadcast")
    await callback.message.answer("Введіть текст повідомлення для розсилання:")

@user_router.message(StateFilter("broadcast"))
async def process_broadcast_message(message: types.Message, state: FSMContext, repo: RequestsRepo, bot: Bot):
    """
    Обработчик рассылки сообщений всем пользователям из базы данных.
    """
    # Текст для рассылки
    broadcast_text = message.text

    try:
        # Получаем всех пользователей из базы данных
        users = await repo.count_users.count_users()  # [(user_id, username), ...]

        # Проверяем, есть ли пользователи
        if not users:
            await message.answer("База даних порожня. Немає кому розсилати повідомлення.")
            await state.clear()
            return

        # Рассылка сообщений
        success_count = 0
        fail_count = 0
        for user_id, username in users:
            try:
                await bot.send_message(chat_id=user_id, text=broadcast_text)
                success_count += 1
            except Exception as e:
                logging.error(f"Не вдалося відправити повідомлення користувачу {user_id}: {e}")
                fail_count += 1

        # Сообщение админу об итогах рассылки
        await message.answer(
            f"Розсилка завершена!\n"
            f"Успішно: {success_count}\n"
            f"Не вдалося: {fail_count}"
        )

    except Exception as e:
        # Логируем ошибку и уведомляем администратора
        logging.error(f"Помилка під час розсилки: {e}")
        await message.answer("Сталася помилка під час розсилання. Спробуйте пізніше.")

    # Очистка состояния
    await state.clear()
