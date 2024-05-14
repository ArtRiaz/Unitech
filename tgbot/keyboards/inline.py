from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


# Keyboards

# New user
def start_keyboard_user():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⛴ Про нас", callback_data="about")], [
            InlineKeyboardButton(text="📝 Регистрация на вакансию", callback_data="register")],

        [InlineKeyboardButton(text="📲 Kонтакты", callback_data="contacts")]
    ]
    )
    return ikb


def contact_keyboard():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📧 Email", callback_data="email")],
        [InlineKeyboardButton(text="📱Телефон", callback_data="phone")],
        [InlineKeyboardButton(text="↩️ Назад в меню", callback_data="back")]])
    return ikb


def admin_kb():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Просмотреть заявки", callback_data="view_requests")],
        [InlineKeyboardButton(text="📈 Количество пользователей", callback_data="view_users")]])

    return ikb


def back():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="↩️ Назад в меню", callback_data="back")]])
    return ikb


def back_admin():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="↩️ Назад в меню", callback_data="back_admin")]])
    return ikb
