import requests
from bs4 import BeautifulSoup
import json

tickets = {}
for page in range(1, 3):
    print(f' ------- Page {page} -------------')
    cookies = {'exam-settings': '%7B%22category%22%3A2%2C%22locale%22%3A%22ru%22%2C%22skin%22%3A%22dark%22%2C%22user%22%3A0%2C%22created%22%3A1726056775%7D'}
    r = requests.get('https://teoria.on.ge/tickets/1/31?page={}'.format(page), cookies=cookies)

    soup = BeautifulSoup(r.text, 'lxml')
    title = soup.title.string
    print(title)

    quotes = soup.find_all('article', class_='ticket-container')
    for quote in quotes:
        ticketID = quote.find('div', class_='t-num').text
        tickets[ticketID] = {
            'title': quote.find('div', class_='t-question').p.span.text
        }
        for quote_answer in quote.find('div', class_='t-cover').find_all('p', class_='t-answer'):
            answer = quote_answer.text.strip().split('\n')
            if len(answer) > 1:
                tickets[ticketID][answer[0]] = answer[2]
                if quote_answer.has_attr('database-is-correct-list'):
                    tickets[ticketID]['correct_answer'] = answer[0]

with open('tickets-adm-original-ru.json', 'w') as f:
    json.dump(tickets, f, indent=4, ensure_ascii=False)