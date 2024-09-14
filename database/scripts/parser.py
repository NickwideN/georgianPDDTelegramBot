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
    :return: Dict of tickets in the format: {
        ticket_id: {
            'title': str,
            'answers': {
                answer_id: str,
                answer_id: str,
            },
            'correct_answer': int
        }
    }
    """
    tickets = {}
    for page in range(1, 92):  # Так как есть только 44 страницы с билетами
        print(f' ------- Parse page {page} -------------')
        soup = get_soup(f'/tickets/0?page={page}', lang_code)

        quotes = soup.find_all('article', class_='ticket-container')
        for quote in quotes:
            ticket_id = int(quote.find('div', class_='t-num').text.replace('#', ''))
            tickets[ticket_id] = {
                'title': quote.find('div', class_='t-question').p.span.text,
                'answers': {},
            }
            for quote_answer in quote.find('div', class_='t-cover').find_all('p', class_='t-answer'):
                answer = quote_answer.text.strip().split('\n')
                answer_id = int(answer[0])
                answer_text = answer[2]
                if len(answer) > 1:
                    tickets[ticket_id]['answers'][answer_id] = answer_text
                    if quote_answer.has_attr('data-is-correct-list'):
                        tickets[ticket_id]['correct_answer'] = answer_id
    return tickets


def get_ticket_topic_relations():
    """
    :return: Dict of ticket-topic relations: {topic_id: [ticket_id, ticket_id,...]}
    """
    relations = {}

    topics = get_topics_ka_lang()
    for topic in topics:
        print(f'======== Parse topic {topic["id"]} ========')
        relations[topic['id']] = []

        soup = get_soup(f'/tickets/0/{topic['id']}')
        page_options = soup.find('select', class_='paginator-select').find_all('option')
        for page_option in page_options:
            page = page_option.attrs['value']
            print(f'------- Parse page {page} -------------')
            soup_page = get_soup(f'/tickets/0/{topic['id']}?page={page}')
            ticket_containers = soup_page.find_all('article', class_='ticket-container')

            for ticket_container in ticket_containers:
                ticket_id = int(ticket_container.find('div', class_='t-num').text.replace('#', ''))
                relations[topic['id']].append(ticket_id)
    return relations


def get_ticket_category_relations():
    relations = {}

    categories = get_categories_ka_lang()
    for category in categories:
        print(f'======== Parse category {category["id"]} ========')
        relations[category['id']] = []

        soup = get_soup(f'/tickets/{category['id']}')
        page_options = soup.find('select', class_='paginator-select').find_all('option')
        for page_option in page_options:
            page = page_option.attrs['value']
            print(f'------- Parse page {page} -------------')
            soup_page = get_soup(f'/tickets/{category['id']}?page={page}')
            ticket_containers = soup_page.find_all('article', class_='ticket-container')

            for ticket_container in ticket_containers:
                ticket_id = int(ticket_container.find('div', class_='t-num').text.replace('#', ''))
                relations[category['id']].append(ticket_id)
    return relations
