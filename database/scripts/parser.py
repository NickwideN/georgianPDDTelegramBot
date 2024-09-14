import requests
from bs4 import BeautifulSoup


def get_soup(url_path: str, lang_code: str = 'ka') -> BeautifulSoup:
    url_domain = 'https://teoria.on.ge'
    cookies: dict[str, str] = {
        'exam-settings': f'%7B%22category%22%3A2%2C%22locale%22%3A%22{lang_code}'
                         f'%22%2C%22skin%22%3A%22dark%22%2C%22user%22%3A0%2C%22created%22%3A1726056775%7D'}
    r = requests.get(url_domain + url_path, cookies=cookies)
    return BeautifulSoup(r.text, 'lxml')


def get_languages():
    languages = []
    settings_lang = get_soup('/tickets').find('li', class_='settings-lang')
    for quote in settings_lang.find_all('li', class_='li-2'):
        languages.append({
            'code': quote.a.attrs['data-value'],
            'description': quote.a.text
        })
    return languages


def get_topics_ka_lang():
    """
    :return: List of topics in the format in georgian: [{'id': int, 'text': str}]
    """
    topics = []
    soup = get_soup('/tickets')
    tickets_topics_list = soup.find('ul', class_='tickets-topics-list')
    for topic in tickets_topics_list.find_all('li'):
        if topic.a.span:
            topics.append({
                'id': int(topic.a.span.text.replace('.', '')),
                'text': topic.a.attrs['title']
            })
    return topics


def get_categories_ka_lang():
    """
    :return: List of categories in the format in georgian: [{'id': int, 'text': str}]
    """
    categories = []
    soup = get_soup('/tickets')
    tickets_cats_list = soup.find('ul', class_='tickets-cats-list')
    for category in tickets_cats_list.find_all('li'):
        code = category.a.find('span', class_='cat-label').text
        categories.append({
            'id': category.attrs['class'][1].split('-')[1],
            'code': code if code != 'AMNEW' else 'AM',  # Небольшой костыль для AMNEW
            'text': category.attrs['title']
        })
    return categories


def get_tickets(lang_code):
    """
    :return: List of tickets in the format: {'ticket_id': {'title': str, 'answer1': str, 'answer2': str, 'correct_answer': str}}
    """
    tickets = {}
    for page in range(1, 92):  # Так как есть только 44 страницы с билетами
        print(f' ------- Parse page {page} -------------')
        soup = get_soup(f'/tickets/0?page={page}', lang_code)

        quotes = soup.find_all('article', class_='ticket-container')
        for quote in quotes:
            ticketID = int(quote.find('div', class_='t-num').text.replace('#', ''))
            tickets[ticketID] = {
                'title': quote.find('div', class_='t-question').p.span.text,
                'answers': {},
                'correct_answer': None
            }
            for quote_answer in quote.find('div', class_='t-cover').find_all('p', class_='t-answer'):
                answer = quote_answer.text.strip().split('\n')
                if len(answer) > 1:
                    tickets[ticketID]['answers'][answer[0]] = answer[2]
                    if quote_answer.has_attr('data-is-correct-list'):
                        tickets[ticketID]['correct_answer'] = answer[0]
    return tickets