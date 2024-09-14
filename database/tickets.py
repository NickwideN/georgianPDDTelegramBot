import json


def get_tickets_translated_ru():
    with open('database/tickets-translated-ru.json_sources', 'r') as file:
        return json.load(file)


def get_tickets_med_original_ru():
    with open('database/tickets-med-original-ru.json_sources', 'r') as file:
        return json.load(file)


def get_tickets_adm_original_ru():
    with open('database/tickets-adm-original-ru.json_sources', 'r') as file:
        return json.load(file)


def get_tickets_original_ru():
    with open('database/tickets-original-ru.json_sources', 'r') as file:
        return json.load(file)


def get_tickets_favorites_original_ru(ticket_numbers: list):
    tickets_original_ru = get_tickets_original_ru()
    return {f'#{ticket_number}': tickets_original_ru[f'#{ticket_number}']
            for ticket_number in ticket_numbers if f'#{ticket_number}' in tickets_original_ru.keys()}
