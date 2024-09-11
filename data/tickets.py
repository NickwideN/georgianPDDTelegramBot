import json


def get_tickets_translated_ru():
    with open('data/tickets-translated-ru.json', 'r') as file:
        return json.load(file)


def get_tickets_med_original_ru():
    with open('data/tickets-med-original-ru.json', 'r') as file:
        return json.load(file)


def get_tickets_adm_original_ru():
    with open('data/tickets-adm-original-ru.json', 'r') as file:
        return json.load(file)


def get_tickets_original_ru():
    with open('data/tickets-original-ru.json', 'r') as file:
        return json.load(file)


def get_tickets_favorites_original_ru(ticket_numbers: list):
    tickets_original_ru = get_tickets_original_ru()
    return {f'#{ticket_number}': tickets_original_ru[f'#{ticket_number}']
            for ticket_number in ticket_numbers if f'#{ticket_number}' in tickets_original_ru.keys()}
