LEXICON_RU: dict[str, str] = {
    '/start': 'Привет! Я выдам билеты ПДД\n\n'
              'Нажми /tickets_med_original_ru для получения билетов ПДД на тему медицины\n'
              'Нажми /tickets_adm_original_ru для получения билетов на тему администрации\n'
              'Нажми /tickets_translated_ru для получения переведенных на русский билетов со страниц 41-44\n'
              'Пришли номера билетов в любом формате, чтобы получить эти билеты в русском оригинальном переводе\n',
    'other_answer': 'Я понимаю только команды /start и /tickets'
}

LEXICON_COMMANDS_RU: dict[str, str] = {
    '/start': 'Запуск бота',
    '/tickets_med_original_ru': 'Выдать список билетов на тему медицины',
    '/tickets_adm_original_ru': 'Выдать список билетов на тему администрации',
    '/tickets_translated_ru': 'Выдать список переведенных на русский билетов со страниц 41-44',
}


def get_text(keyword: str) -> str:
    return LEXICON_RU[keyword] if keyword in LEXICON_RU else keyword
