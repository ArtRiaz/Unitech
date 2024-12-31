from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


# Keyboards

# New user
def start_keyboard_user():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="☀️ О Компанii", callback_data="about")],
        [InlineKeyboardButton(text="📒 Нашi рiшення", callback_data="catalog")],
        [InlineKeyboardButton(text="📝 Зв'язатись з нами", callback_data="register")],
        [InlineKeyboardButton(text="📱 Розрахувати вашу систему", callback_data="count")],
        [InlineKeyboardButton(text="📲 Kонтакти", callback_data="contacts")]
    ]
    )
    return ikb


def contact_keyboard():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Instagram", url="https://instagram.com")],
        [InlineKeyboardButton(text="Facebook", url="https://facebook.com")],
        [InlineKeyboardButton(text="📱Телефон", callback_data="phone")],
        [InlineKeyboardButton(text="📧 Email", callback_data="email")],
        [InlineKeyboardButton(text="📍Геолокацiя", callback_data="geo")],
        [InlineKeyboardButton(text="🌎 Сайт", url="https://unitech.onyxer.agency/")],
        [InlineKeyboardButton(text="☎️ Зв'язок з нами онлайн", callback_data='online')],
        [InlineKeyboardButton(text="↩️ Назад у меню", callback_data="back")]])
    return ikb


def admin_kb():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Просмотреть заявки", callback_data="view_requests")],
        [InlineKeyboardButton(text="📈 Количество пользователей", callback_data="view_users")]])

    return ikb


def back():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="↩️ Назад у меню", callback_data="back")]])
    return ikb


def back_admin():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="↩️ Назад у меню", callback_data="back_admin")]])
    return ikb


def pagination():
    ikb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⏪", callback_data="left"),
                                                 InlineKeyboardButton(text="⏩", callback_data="right")],
                                                [InlineKeyboardButton(text="↩️ Назад у меню", callback_data="back")]])

    return ikb
