import re

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from database import tickets

from lexicon.lexicon_ru import LEXICON_RU
from keyboards.keyboards import create_inline_kb

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'])


@router.message(Command('tickets_med_original_ru'))
async def process_get_tickets_command(message: Message):
    await message.answer(text="Сейчас тебе придет список мед билетов ПДД")
    for ticket_number, ticket_info in tickets.get_tickets_med_original_ru().items():
        await message.answer(**ticket_post(ticket_info, ticket_number))


@router.message(Command('tickets_adm_original_ru'))
async def process_get_tickets_command(message: Message):
    await message.answer(text="Сейчас тебе придет список билетов администрации ПДД")
    for ticket_number, ticket_info in tickets.get_tickets_adm_original_ru().items():
        await message.answer(**ticket_post(ticket_info, ticket_number))


@router.message(Command('tickets_translated_ru'))
async def process_get_tickets_command(message: Message):
    await message.answer(text="Сейчас тебе придет список переведенных билетов ПДД со страницы 41-44")
    for ticket_number, ticket_info in tickets.get_tickets_translated_ru().items():
        await message.answer(**ticket_post(ticket_info, ticket_number))


@router.message(F.text)
async def process_get_tickets_command(message: Message):
    await message.answer(text="Сейчас тебе придет список указанных билетов")

    ticket_numbers = [int(num) for num in re.findall(r'\b\d+\b', message.text)]
    await message.answer(text='Билеты, которые ты запросил: ' + str(ticket_numbers))

    tickets_favorites_original_ru = tickets.get_tickets_favorites_original_ru(ticket_numbers)
    await message.answer(text='Билеты, которые не были найдены в базе: '
                              + str([ticket_number for ticket_number in ticket_numbers
                                     if f'#{ticket_number}' not in tickets_favorites_original_ru.keys()]))

    if not tickets_favorites_original_ru:
        await message.answer(text="Ни одного билета не найдено в базе")
        return
    else:
        for ticket_number, ticket_info in tickets_favorites_original_ru.items():
            await message.answer(**ticket_post(ticket_info, ticket_number))


def ticket_post(ticket_info, ticket_number):
    answers = []
    inline_buttons = {}
    for i in range(0, 5):
        if str(i) in ticket_info.keys():
            key = ['ans', str(i), '1' if int(ticket_info['correct_answer']) == i else '0']
            inline_buttons['_'.join(key)] = f'Ответ {i}'
            answers.append(f'{i}. ' + ticket_info[str(i)])
    return {
        'text': f"<b>Билет {ticket_number}</b>: \n\n{ticket_info['title']} \n\n Ответы:\n" + '\n'.join(answers),
        'reply_markup': create_inline_kb(1, **inline_buttons)
    }


@router.callback_query(F.data.regexp(r"ans_(\d+)_1$"))
async def process_button_click(callback: CallbackQuery):
    await callback.answer(text=f"Это правильный ответ!")


@router.callback_query(F.data.regexp(r"ans_(\d+)_0$"))
async def process_button_click(callback: CallbackQuery):
    await callback.answer(text=f"Это неправильный ответ!")


@router.callback_query()
async def process_button_click(callback: CallbackQuery):
    await callback.answer(text=f"Ответ не обработан")
