from aiogram import types, Router, F
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

# Инициализация Router
catalog_router = Router()


# CallbackData для управления пагинацией
class PaginationCallback(CallbackData, prefix="pagination"):
    action: str  # "left" или "right"
    page: int  # Номер страницы


# Данные каталога (можно заменить на загрузку из базы)
catalog_items = [
    {"photo": "tgbot/card.png", "caption": "Квартири"},
    {"photo": "tgbot/card2.png", "caption": "Приватний бiзнес"},
    {"photo": "tgbot/card3.png", "caption": "Резиденцii"},
    {"photo": "tgbot/card4.png", "caption": "Iндустрiалiзацiя"}
]


# Функция для генерации клавиатуры пагинации
def pagination_keyboard(current_page: int, total_pages: int):
    navigation_buttons = []

    if current_page > 0:
        navigation_buttons.append(
            InlineKeyboardButton(
                text="Назад ⏪",
                callback_data=PaginationCallback(action="left", page=current_page - 1).pack()
            )
        )
    if current_page < total_pages - 1:
        navigation_buttons.append(
            InlineKeyboardButton(
                text="Далi ⏩",
                callback_data=PaginationCallback(action="right", page=current_page + 1).pack()
            )
        )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            navigation_buttons,  # Кнопки навигации на первой строке
            [
                InlineKeyboardButton(
                    text="↩️ Назад у меню",
                    callback_data="back"
                )
            ]  # Кнопка "Назад" на отдельной строке
        ]
    )


# Обработчик начального каталога
@catalog_router.callback_query(F.data == "catalog")
async def show_catalog(callback_query: types.CallbackQuery):
    page = 0  # Начальная страница
    await send_catalog_page(callback_query.message, page)
    await callback_query.answer()


# Обработчик пагинации
@catalog_router.callback_query(PaginationCallback.filter())
async def paginate_catalog(callback_query: types.CallbackQuery, callback_data: PaginationCallback):
    page = callback_data.page  # Получаем текущую страницу из callback_data
    await send_catalog_page(callback_query.message, page)
    await callback_query.answer()


# Функция для отправки страницы каталога
async def send_catalog_page(message: types.Message, page: int):
    total_pages = len(catalog_items)
    item = catalog_items[page]
    keyboard = pagination_keyboard(page, total_pages)
    # Обновляем сообщение с новым контентом
    await message.edit_media(
        media=types.InputMediaPhoto(media=FSInputFile(item["photo"]), caption=item["caption"]),
        reply_markup=keyboard
    )
