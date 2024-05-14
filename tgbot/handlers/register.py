from aiogram import types, F, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from infrastructure.database.repo.request import RequestsRepo
import asyncio

register_router = Router()


class Form(StatesGroup):
    name = State()
    age = State()
    job = State()
    contact = State()
    exp = State()


@register_router.message(Command("cancel"))
async def cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Регистрация отменена, нажмите /start что бы начать заново")


@register_router.callback_query(F.data == "register")
async def about(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.name)
    await callback_query.message.answer("Регистрация на вакансию\n"
                                        "Введите ваше имя или нажмите /cancel для отмены")
    await callback_query.answer()
    # Запуск таймера сброса состояния
    await reset_state_timer(state, callback_query.message)


async def reset_state_timer(state: FSMContext, message: types.Message):
    """Устанавливает таймер для сброса состояния"""
    await asyncio.sleep(120)  # Подождать 2 минуту
    if not await state.get_state():  # Проверить, что состояние все еще активно
        return
    await state.clear()  # Сброс состояния
    await message.answer("Время ожидания истекло, регистрация отменена.\n"
                         " Нажми на команду /start")


@register_router.message(StateFilter(Form.name))
async def name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.age)
    await message.answer("Введите ваш возраст или нажмите /cancel для отмены")
    await reset_state_timer(state, message)


@register_router.message(StateFilter(Form.age))
async def age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Form.job)
    await message.answer("Введите вашу специальность или нажмите /cancel для отмены")
    await reset_state_timer(state, message)


@register_router.message(StateFilter(Form.job))
async def job(message: types.Message, state: FSMContext):
    await state.update_data(job=message.text)
    await state.set_state(Form.contact)
    await message.answer("Введите ваш контактный номер или email и или нажмите /cancel для отмены")
    await reset_state_timer(state, message)


@register_router.message(StateFilter(Form.contact))
async def contact(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await state.set_state(Form.exp)
    await message.answer("Введите ваш опыт работы или нажмите /cancel для отмены")
    await reset_state_timer(state, message)


@register_router.message(StateFilter(Form.exp))
async def exp(message: types.Message, state: FSMContext, repo: RequestsRepo, config):
    await state.update_data(exp=message.text)
    data = await state.get_data()
    await repo.register.get_or_create_register(
        name=data['name'],
        age=data['age'],
        contact=data['contact'],
        profession=data['job'],
        expirience=data['exp']
    )

    await message.answer(f"Спасибо {data['name']} за регистрацию!\n"
                         f"Мы свяжемся с Вами в ближайшее время\n"
                         f"Нажмите /start для продолжения работы с ботом")

    await message.bot.send_message(chat_id=951140653, text=f"Новая заявка на вакансию\n"
                                                           f"Имя: {data['name']}\n"
                                                           f"Специальность: {data['age']}\n"
                                                           f"Контакт: {data['job']}\n"
                                                           f"Опыт работы: {data['exp']}\n"
                                                           f"Контактный номер: {data['contact']}")

    await state.clear()
