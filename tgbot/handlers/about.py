from aiogram import types, F, Router
from tgbot.keyboards.inline import back
from aiogram.types import FSInputFile

about_router = Router()


@about_router.callback_query(F.data == "about")
async def about(callback_query: types.CallbackQuery):
    await callback_query.message.answer_photo(photo=FSInputFile("tgbot/logoo.jpeg"),
                                              caption="-Компания 'Литсома', г.Клайпеда,"
                                                      "Литва осуществляет деятельность в отрасли "
                                                      "судостроение/судоремонт,"
                                                      "трубопроводные системы (в том числе промышленные),"
                                                      "ремонт промышленного оборудования, металлоконструкций,"
                                                      "корпусные ремонтные работы, модернизация судна,"
                                                      "на проектах в Литве, , Финляндии, Швеции, Нидерландах, Дании, "
                                                      "Франции.",
                                              reply_markup=back())
    await callback_query.answer()
