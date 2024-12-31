import base64
from aiogram import types, F, Router, Bot
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from infrastructure.database.repo.request import RequestsRepo
import asyncio
from io import BytesIO
from aiogram.types import FSInputFile, InputFile, BufferedInputFile
import logging
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

register_router = Router()


class Form(StatesGroup):
    name = State()
    contact = State()
    pdf_file = State()
    comment = State()


@register_router.callback_query(F.data == "cancel")
async def inline_cancel(callback_query: types.CallbackQuery, state: FSMContext):
    # Создаем инлайн-кнопку "Start"
    start_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Start", callback_data="start")]
        ]
    )
    await state.clear()
    await callback_query.message.edit_text("Реєстрацію скасовано, натисніть start щоб почати знову",
                                           reply_markup=start_button)
    await callback_query.answer()


@register_router.callback_query(F.data == "continue")
async def handle_continue(callback_query: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()

    if current_state == Form.contact:
        # Пропуск ввода контактных данных
        await state.update_data(contact=None)
        await state.set_state(Form.pdf_file)
        await callback_query.message.answer("Прикріпіть PDF файл з планом свого об'єкта, якщо у вас є. "
                                            "Якщо ні, натисніть Пропустити.",
                                            reply_markup=InlineKeyboardMarkup(
                                                inline_keyboard=[
                                                    [InlineKeyboardButton(text="Повернутись ↩️", callback_data="cancel")],
                                                    [InlineKeyboardButton(text="Пропустити", callback_data="continue")]
                                                ]
                                            ))
    elif current_state == Form.pdf_file:
        # Пропуск загрузки PDF
        await state.update_data(pdf_file=None)
        await state.set_state(Form.comment)
        await callback_query.message.answer("Введіть короткий коментар або натиснiть Повернутись.",
                                            reply_markup=InlineKeyboardMarkup(
                                                inline_keyboard=[
                                                    [InlineKeyboardButton(text="Повернутись ↩️", callback_data="cancel")]
                                                ]
                                            ))
    await callback_query.answer()


@register_router.callback_query(F.data == "register")
async def about(callback_query: types.CallbackQuery, state: FSMContext):
    # Создаем инлайн-кнопку "Cancel"
    cancel_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Повернутись ↩️", callback_data="cancel")]
        ]
    )

    await state.set_state(Form.name)
    await callback_query.message.answer(
        "Введіть ім'я або натисніть кнопку нижче для скасування:",
        reply_markup=cancel_button
    )
    await callback_query.answer()
    # Запуск таймера сброса состояния
    await reset_state_timer(state, callback_query.message)


async def reset_state_timer(state: FSMContext, message: Message, timeout: int = 120):
    start_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Start", callback_data="start")]
        ]
    )
    """
    Устанавливает таймер для сброса состояния.

    :param state: FSMContext - текущий контекст состояния.
    :param message: Message - сообщение для ответа пользователю.
    :param timeout: int - время ожидания перед сбросом состояния (в секундах).
    """
    try:
        logging.info(f"Запуск таймера сброса состояния для пользователя {message.from_user.id}")
        for _ in range(timeout):
            await asyncio.sleep(1)
            if not await state.get_state():  # Если состояние уже очищено
                logging.info(f"Состояние пользователя {message.from_user.id} сброшено до окончания таймера.")
                return

        # Если таймер истёк, состояние всё ещё активно
        if await state.get_state():
            logging.info(f"Таймер истёк для пользователя {message.from_user.id}, сбрасываем состояние.")
            await state.clear()
            await message.answer(
                "Час для регiстрацii вичерпан, регiстрацiя вiдхилина.\n"
                "Натисни на команду start", reply_markup=start_button
            )
    except Exception as e:
        logging.error(f"Ошибка при выполнении таймера сброса состояния: {e}")


@register_router.message(StateFilter(Form.name))
async def name(message: types.Message, state: FSMContext):
    # Создаем инлайн-кнопку "Cancel"
    cancel_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Повернутись ↩️", callback_data="cancel")]
        ]
    )
    # Проверяем, что сообщение состоит только из букв и длина не более 20 символов
    if not message.text.isalpha():
        await message.answer("Ім'я повинно містити лише літери. Будь ласка, спробуйте ще раз.")
        return
    if len(message.text) > 20:
        await message.answer("Ім'я повинно бути не довше 20 символів. Будь ласка, спробуйте ще раз.")
        return

    await state.update_data(name=message.text)
    await state.set_state(Form.contact)
    await message.answer("Введіть контактний номер або натисніть кнопку нижче для скасування:", reply_markup=cancel_button)
    await reset_state_timer(state, message)


@register_router.message(StateFilter(Form.contact))
async def contact(message: types.Message, state: FSMContext):
    # Создаем инлайн-кнопку "Cancel"
    cancel_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Повернутись ↩️", callback_data="cancel")],
            [InlineKeyboardButton(text="Пропустить", callback_data="continue")]
        ]
    )
    # Проверяем, что сообщение состоит только из цифр и длина не более 20 символов
    if not message.text.isdigit():
        await message.answer("Контактний номер повинен містити лише цифри. Будь ласка, спробуйте ще раз.")
        return
    if len(message.text) > 20:
        await message.answer("Контактний номер повинен бути не довшим за 20 символів. Будь ласка, спробуйте ще раз.")
        return

    await state.update_data(contact=message.text)
    await state.set_state(Form.pdf_file)
    await message.answer("Прикріпіть PDF файл з планом свого об'єкта, якщо у вас є. Якщо ні, натисніть /continue.\n"
                         "Якщо хочете скасувати заявку, натисніть скасування:", reply_markup=cancel_button)
    await reset_state_timer(state, message)

@register_router.message(StateFilter(Form.pdf_file))
async def pdf_file_handler(message: types.Message, state: FSMContext, bot: Bot):
    # Создаем инлайн-кнопку "Cancel"
    cancel_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Повернутись ↩️", callback_data="cancel")],
            [InlineKeyboardButton(text="Пропустить", callback_data="continue")]
        ]
    )

    cancel_buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Повернутись ↩️", callback_data="cancel")]
        ]
    )

    # Если пользователь решил пропустить загрузку
    if message.text == "/continue":
        await state.update_data(pdf_file=None)

    # Если пришёл документ и он PDF
    elif message.document:
        if message.document.mime_type == "application/pdf":
            file_id = message.document.file_id
            logging.info(file_id)
            file = await bot.get_file(file_id)  # Получение информации о файле
            logging.info(file)
            file_stream: BytesIO = await bot.download_file(file.file_path)  # Загрузка файла как поток
            logging.info(file_stream)
            pdf_bytes = file_stream.read()  # Чтение содержимого потока в байты

            # Кодируем в Base64
            pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

            # Сохраняем закодированные данные в состоянии
            await state.update_data(pdf_file=pdf_base64)
        else:
            # Если документ не PDF, отправляем сообщение с ошибкой
            await message.answer("Будь ласка, прикрепить файл у форматі PDF або натиснiть continue щоб пропустити\n"
                                 "Якщо вiдмiнити заявку натиснiть скасування:", reply_markup=cancel_button)
            return
    else:
        # Если не документ и не /continue, просим повторить
        await message.answer("Будь ласка, прикрепить файл у форматі PDF або натиснiть continue щоб пропустити\n"
                             "Якщо вiдмiнити заявку натиснiть скасування:", reply_markup=cancel_button)
        return

    await state.set_state(Form.comment)
    await message.answer("Введите короткий комментар або натиснiть скасування", reply_markup=cancel_buttons)
    await reset_state_timer(state, message)


@register_router.message(StateFilter(Form.comment))
async def exp(message: types.Message, state: FSMContext, repo: RequestsRepo, config):
    # Создаем инлайн-кнопку "Start"
    start_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Start", callback_data="start")]
        ]
    )

    # Проверка длины комментария
    if len(message.text) > 50:
        await message.answer("Коментар має бути не довший за 50 символів. Спробуйте ще раз.")
        return

    await state.update_data(comment=message.text)

    # Получаем все данные из состояния
    data = await state.get_data()

    # Инициализация переменной pdf
    pdf: BufferedInputFile | None = None

    # Проверяем и декодируем PDF файл
    pdf_file = data.get('pdf_file')  # Получаем значение pdf_file

    if pdf_file is not None and isinstance(pdf_file, str):
        # Если файл сохранён как строка Base64, декодируем его
        pdf_file = base64.b64decode(pdf_file)
        pdf = BufferedInputFile(pdf_file, filename="file1.pdf")

    # Вставляем запись в базу данных
    await repo.register.get_or_create_register(
        name=data['name'],
        contact=data['contact'],
        pdf_file=pdf_file,  # Передаем байты
        comment=data['comment']
    )

    # Сообщение пользователю
    await message.answer(
        f"Дякуємо {data['name']} за регiстрацiю!\n"
        f"Мы зв'яжемося з Вами найближчим часом\n"
        f"Натиснiть start для продовження роботи з ботом",
        reply_markup=start_button
    )

    # Отправляем документ, если он существует
    if pdf is not None:
        await message.bot.send_document(
            chat_id=-1002185862798,
            document=pdf,
            caption=(
                f"Нова заявка\n\n"
                f"Iмя: {data['name']}\n\n"
                f"Контактний номер: {data['contact']}\n\n"
                f"Коментар: {data['comment']}"
            )
        )
    else:
        await message.bot.send_message(chat_id=-1002185862798,
                                       text=f"Нова заявка\n\n"
                                            f"Iмя: {data['name']}\n\n"
                                            f"Контактний номер: {data['contact']}\n\n"
                                            f"Коментар: {data['comment']}")

    # Очистка состояния
    await state.clear()