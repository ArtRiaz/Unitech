from aiogram import types, F, Router, Bot
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from infrastructure.database.repo.request import RequestsRepo
import asyncio
from aiogram.types import FSInputFile, InputFile, BufferedInputFile
import logging
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

count_router = Router()

cancel_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Повернутись ↩️", callback_data="cancel")],
        [InlineKeyboardButton(text="Пропустить", callback_data="cont")]
    ]
)


class CountForm(StatesGroup):
    adress_type_object = State()
    electric_time = State()
    tarif = State()
    crowl = State()
    type_crowl = State()
    type_system = State()
    power_station = State()
    acamulator = State()
    phone = State()
    email = State()


@count_router.callback_query(F.data == "cancels")
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



async def reset_state_timer(state: FSMContext, message: Message, timeout: int = 800):
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

@count_router.callback_query(F.data == "cont")
async def skip_step(callback_query: types.CallbackQuery, state: FSMContext, repo: RequestsRepo):
    """
    Обработчик кнопки 'Пропустить'.
    Переводит на следующее состояние и записывает 'None' в текущие данные.
    """
    current_state = await state.get_state()

    # Логика обработки для каждого состояния
    if current_state == CountForm.adress_type_object.state:

        await state.update_data(adress_type_object=None)
        await state.set_state(CountForm.electric_time)
        await callback_query.message.answer(
            "Введіть річне енергоспоживання та години роботи споживання, або натисніть скасування чи пропустiть:",
            reply_markup=cancel_buttons
        )
    elif current_state == CountForm.electric_time.state:

        await state.update_data(electric_time=None)
        await state.set_state(CountForm.tarif)
        await callback_query.message.answer(
            "Введiть актуальний тариф на електроенергію, або натисніть скасування чи пропустiть",
            reply_markup=cancel_buttons
        )
    elif current_state == CountForm.tarif.state:

        await state.update_data(tarif=None)
        await state.set_state(CountForm.crowl)
        await callback_query.message.answer(
            "Введiть площю даху, придатна для встановлення, або натиснiть скасування чи пропустiть",
            reply_markup=cancel_buttons
        )
    elif current_state == CountForm.crowl.state:

        await state.update_data(crowl=None)
        await state.set_state(CountForm.type_crowl)
        await callback_query.message.answer(
            "Введiть тип даху (односхилий, двосхилий, плаский), або натиснiть скасування чи пропустiть",
            reply_markup=cancel_buttons
        )
    elif current_state == CountForm.type_crowl.state:

        await state.update_data(type_crowl=None)
        await state.set_state(CountForm.type_system)
        await callback_query.message.answer(
            "Введiть тип системи (on grid або hybrid), або натиснiть скасування чи пропустiть",
            reply_markup=cancel_buttons
        )
    elif current_state == CountForm.type_system.state:

        await state.update_data(type_system=None)
        await state.set_state(CountForm.power_station)
        await callback_query.message.answer(
            "Введiть потужність станції за бажанням клієнта в кВт, або натиснiть скасування чи пропустiть",
            reply_markup=cancel_buttons
        )
    elif current_state == CountForm.power_station.state:

        await state.update_data(power_station=None)
        await state.set_state(CountForm.acamulator)
        await callback_query.message.answer(
            "Введiть чи потрібні акумулятори в системі та їхня ємність, або натиснiть скасування чи пропустiть",
            reply_markup=cancel_buttons
        )
    elif current_state == CountForm.acamulator.state:
        await state.update_data(acamulator=None)
        await state.set_state(CountForm.phone)
        await callback_query.message.answer(
            "Введiть контактний номер, або натиснiть скасування чи пропустiть",
            reply_markup=cancel_buttons
        )
    elif current_state == CountForm.phone.state:
        await state.update_data(phone=None)
        await state.set_state(CountForm.email)
        await callback_query.message.answer(
            "Введiть контактний email, або натиснiть скасування чи пропустiть",
            reply_markup=cancel_buttons
        )
    elif current_state == CountForm.email.state:
        # Если это последний шаг, очищаем состояние и отправляем финальное сообщение.
        await state.update_data(email=None)

        # Получаем все данные из состояния
        data = await state.get_data()

        # Вставляем запись в базу данных
        await repo.count.get_or_create_register(
            adress_type_object=data['adress_type_object'],
            electric_time=data['electric_time'],
            tarif=data['tarif'],
            crowl=data['crowl'],
            type_crowl=data['type_crowl'],
            type_system=data['type_system'],
            power_station=data['power_station'],
            acamulator=data['acamulator'],
            phone=data['phone'],
            email=data['email'],
        )



        await callback_query.message.bot.send_message(chat_id=-1002185862798,
                                       text=f"Нова заявка для розрахування системи\n\n"
                                            f"Адреса та тип об'єкту: {data['adress_type_object']}\n\n"
                                            f"Річне енергоспоживання та години роботи: {data['electric_time']}\n\n"
                                            f"Актуальний тариф на електроенергію: {data['tarif']}\n\n"
                                            f"Площю даху, придатна для встановлення: {data['crowl']}\n\n"
                                            f"Тип даху: {data['type_crowl']}\n\n"
                                            f"Тип системи: {data['type_system']}\n\n"
                                            f"Акумулятори в системі та їхня ємність: {data['acamulator']}\n\n"
                                            f"Контактний номер: {data['phone']}\n\n"
                                            f"Контактний email: {data['email']}")

        # Очистка состояния

        await state.clear()
        await callback_query.message.answer(
            "Дякуємо за регiстрацiю! Натиснiть start для початку нового запиту.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="Start", callback_data="start")]]
            )
        )
    await callback_query.answer()



@count_router.callback_query(F.data == "count")
async def about(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(CountForm.adress_type_object)
    await callback_query.message.answer(
        "Введіть адресу та тип об'єкту або натисніть кнопку нижче для повернення чи пропустiть:",
        reply_markup=cancel_buttons
    )
    await callback_query.answer()
    # Запуск таймера сброса состояния
    await reset_state_timer(state, callback_query.message)


@count_router.message(StateFilter(CountForm.adress_type_object))
async def name(message: types.Message, state: FSMContext):
    if len(message.text) > 50:
        await message.answer("Повинно бути не довше 50 символів. Будь ласка, спробуйте ще раз.")
        return

    await state.update_data(adress_type_object=message.text)
    await state.set_state(CountForm.electric_time)
    await message.answer("Введіть річне енергоспоживання та години роботи споживання (наприклад, з 8:00 до 17:00, "
                         "якщо це магазин),або натисніть кнопку скасування чи пропустiть:", reply_markup=cancel_buttons)
    await reset_state_timer(state, message)


@count_router.message(StateFilter(CountForm.electric_time))
async def contact(message: types.Message, state: FSMContext):
    if len(message.text) > 50:
        await message.answer("Контактний номер повинен бути не довшим за 50 символів. Будь ласка, спробуйте ще раз.")
        return

    await state.update_data(electric_time=message.text)
    await state.set_state(CountForm.tarif)
    await message.answer("Введiть актуальний тариф на електроенергію, або натисніть кнопку скасування чи пропустiть",
                         reply_markup=cancel_buttons)
    await reset_state_timer(state, message)


@count_router.message(StateFilter(CountForm.tarif))
async def pdf_file_handler(message: types.Message, state: FSMContext):
    if len(message.text) > 50:
        await message.answer("Контактний номер повинен бути не довшим за 50 символів. Будь ласка, спробуйте ще раз.")
        return
    await state.update_data(tarif=message.text)
    await state.set_state(CountForm.crowl)
    await message.answer("Введiть площю даху, придатна для встановлення, або натиснiть скасування чи пропустiть ",
                         reply_markup=cancel_buttons)
    await reset_state_timer(state, message)


@count_router.message(StateFilter(CountForm.crowl))
async def pdf_file_handler(message: types.Message, state: FSMContext):
    if len(message.text) > 40:
        await message.answer("Контактний номер повинен бути не довшим за 40 символів. Будь ласка, спробуйте ще раз.")
        return
    await state.update_data(crowl=message.text)
    await state.set_state(CountForm.type_crowl)
    await message.answer("Введiть тип даху (односхилий, двосхилий, плаский та матеріал, або натиснiть скасування чи "
                         "пропустiть",
                         reply_markup=cancel_buttons)
    await reset_state_timer(state, message)


@count_router.message(StateFilter(CountForm.type_crowl))
async def pdf_file_handler(message: types.Message, state: FSMContext):
    if len(message.text) > 40:
        await message.answer("Контактний номер повинен бути не довшим за 40 символів. Будь ласка, спробуйте ще раз.")
        return
    await state.update_data(type_crowl=message.text)
    await state.set_state(CountForm.type_system)
    await message.answer("Введiть тип системи (on grid или hybrid), або натиснiть скасування чи "
                         "пропустiть",
                         reply_markup=cancel_buttons)
    await reset_state_timer(state, message)


@count_router.message(StateFilter(CountForm.type_system))
async def pdf_file_handler(message: types.Message, state: FSMContext):
    if len(message.text) > 40:
        await message.answer("Контактний номер повинен бути не довшим за 40 символів. Будь ласка, спробуйте ще раз.")
        return
    await state.update_data(type_system=message.text)
    await state.set_state(CountForm.power_station)
    await message.answer("Введiть потужність станції за бажанням клієнта в кВт, або натиснiть скасування чи "
                         "пропустiть",
                         reply_markup=cancel_buttons)
    await reset_state_timer(state, message)


@count_router.message(StateFilter(CountForm.power_station))
async def pdf_file_handler(message: types.Message, state: FSMContext):
    if len(message.text) > 40:
        await message.answer("Контактний номер повинен бути не довшим за 40 символів. Будь ласка, спробуйте ще раз.")
        return
    await state.update_data(power_station=message.text)
    await state.set_state(CountForm.acamulator)
    await message.answer("Введiть чи потрібні акумулятори в системі та їхня ємність, або натиснiть скасування чи "
                         "пропустiть",
                         reply_markup=cancel_buttons)
    await reset_state_timer(state, message)


@count_router.message(StateFilter(CountForm.acamulator))
async def pdf_file_handler(message: types.Message, state: FSMContext):
    if len(message.text) > 30:
        await message.answer("Контактний номер повинен бути не довшим за 30 символів. Будь ласка, спробуйте ще раз.")
        return
    await state.update_data(acamulator=message.text)
    await state.set_state(CountForm.phone)
    await message.answer("Введiть контактний номер, або натиснiть скасування чи "
                         "пропустiть",
                         reply_markup=cancel_buttons)
    await reset_state_timer(state, message)


@count_router.message(StateFilter(CountForm.phone))
async def pdf_file_handler(message: types.Message, state: FSMContext):
    if len(message.text) > 15:
        await message.answer("Контактний номер повинен бути не довшим за 15 символів. Будь ласка, спробуйте ще раз.")
        return
    await state.update_data(phone=message.text)
    await state.set_state(CountForm.email)
    await message.answer("Введiть контактний email, або натиснiть скасування чи "
                         "пропустiть",
                         reply_markup=cancel_buttons)
    await reset_state_timer(state, message)


@count_router.message(StateFilter(CountForm.email))
async def email(message: types.Message, state: FSMContext, repo: RequestsRepo, config):
    start_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Start", callback_data="start")]
        ]
    )

    # Проверка длины комментария
    if len(message.text) > 30:
        await message.answer("Коментар має бути не довший за 30 символів. Спробуйте ще раз.")
        return
    await state.update_data(email=message.text)

    # Получаем все данные из состояния
    data = await state.get_data()

    # Вставляем запись в базу данных
    await repo.count.get_or_create_register(
        adress_type_object=data['adress_type_object'],
        electric_time=data['electric_time'],
        tarif=data['tarif'],
        crowl=data['crowl'],
        type_crowl=data['type_crowl'],
        type_system=data['type_system'],
        power_station=data['power_station'],
        acamulator=data['acamulator'],
        phone=data['phone'],
        email=data['email'],
    )

    # Сообщение пользователю
    await message.answer(
        f"Дякуємо за регiстрацiю!\n"
        f"Мы зв'яжемося з Вами найближчим часом\n"
        f"Натиснiть start для продовження роботи з ботом",
        reply_markup=start_button
    )

    await message.bot.send_message(chat_id=-1002185862798,
                                   text=f"Нова заявка для розрахування системи\n\n"
                                        f"Адреса та тип об'єкту: {data['adress_type_object']}\n\n"
                                        f"Річне енергоспоживання та години роботи: {data['electric_time']}\n\n"
                                        f"Актуальний тариф на електроенергію: {data['tarif']}\n\n"
                                        f"Площю даху, придатна для встановлення: {data['crowl']}\n\n"
                                        f"Тип даху: {data['type_crowl']}\n\n"
                                        f"Тип системи: {data['type_system']}\n\n"
                                        f"Акумулятори в системі та їхня ємність: {data['acamulator']}\n\n"
                                        f"Контактний номер: {data['phone']}\n\n"
                                        f"Контактний email: {data['email']}")

    # Очистка состояния
    await state.clear()
