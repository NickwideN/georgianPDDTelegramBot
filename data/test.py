import json

with open('tickets-ge.json', 'r') as file:
    tickets_ge = json.load(file)

with open('tickets-translated-ru.json', 'r') as file:
    tickets_ru = json.load(file)

tickets_ru_numbers = tickets_ru.keys()
print('Билеты Ge, которых нет в RU:')
for ticket_ge_number, ticket_ge in tickets_ge.items():
    if ticket_ge_number not in tickets_ru_numbers:
        print(ticket_ge_number)
    else:
        for key in ticket_ge.keys():
            if key not in tickets_ru[ticket_ge_number]:
                print(f'Билет {ticket_ge_number}, ключ {key}')

print('------------')

tickets_ge_numbers = tickets_ge.keys()
print('Билеты RU, которых нет в GE:')
for ticket_ru_number, ticket_ru in tickets_ru.items():
    if ticket_ru_number not in tickets_ge_numbers:
        print(ticket_ru_number)
    else:
        for key in ticket_ru.keys():
            if key not in tickets_ge[ticket_ru_number]:
                print(f'Билет {ticket_ru_number}, ключ {key}')
