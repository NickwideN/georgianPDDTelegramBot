import json
import parser


def create_languages_json():
    languages = parser.get_languages()
    with open('json_sources/languages.json', 'w') as f:
        json.dump(languages, f, indent=4, ensure_ascii=False)


def get_languages():
    with open('json_sources/languages.json', 'r') as file:
        return json.load(file)


def create_topics_json():
    languages = get_languages()
    topics = {}
    for topic_ka in parser.get_topics_ka_lang():
        topics[topic_ka['id']] = {
            'ka': topic_ka['text']
        }
        for lang in languages:
            if lang['code'] != 'ka':
                topics[topic_ka['id']][lang['code']] = ''

    with open('json_sources/topics.json', 'w') as f:
        json.dump(topics, f, indent=4, ensure_ascii=False)


def get_topics_json():
    with open('json_sources/topics.json', 'r') as file:
        return json.load(file)


def create_categories_json():
    languages = get_languages()
    category = {}
    for category_ka in parser.get_categories_ka_lang():
        category[category_ka['id']] = {
            'code': category_ka['code'],
            'ka': category_ka['text']
        }
        for lang in languages:
            if lang['code'] != 'ka':
                category[category_ka['id']][lang['code']] = ''

    with open('json_sources/categories.json', 'w') as f:
        json.dump(category, f, indent=4, ensure_ascii=False)

def get_categories_json():
    with open('json_sources/categories.json', 'r') as file:
        return json.load(file)
