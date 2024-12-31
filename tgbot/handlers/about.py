from aiogram import types, F, Router
from tgbot.keyboards.inline import back
from aiogram.types import FSInputFile

about_router = Router()


@about_router.callback_query(F.data == "about")
async def about(callback_query: types.CallbackQuery):
    await callback_query.message.answer_photo(photo=FSInputFile("tgbot/about-company.jpg"),
                                              caption="Unitech Solar — компанія, яка створена з метою впровадження "
                                                      "інноваційних та ефективних рішень сонячної енергетики в "
                                                      "Україні.\n"
                                                      "Наші фахівці навчалися в Індії та Китаї, що дало нам "
                                                      "можливість інтегрувати найкращі світові практики у локальні "
                                                      "проекти. Завдяки тісному партнерству з міжнародними колегами, "
                                                      "ми маємо доступ до передових технологій та методів.\n"
                                                      "Ми орієнтовані на індивідуальний підхід до кожного проекту, "
                                                      "надаючи наші знання та досвід для розробки максимально "
                                                      "ефективних та стійких рішень для бізнесу та приватних клієнтів.",
                                              reply_markup=back())
    await callback_query.message.edit_reply_markup()
    await callback_query.message.delete()
    await callback_query.answer()


