from aiogram import Router
from aiogram.types import Message

from lexicon.lexicon_ru import LEXICON_RU

router = Router()


@router.message()
async def send_answer(message: Message):
    await message.answer(LEXICON_RU['other_answer'])
