from database.connection import connect_to_db
import json_utils
import parser
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] #%(levelname)-8s %(filename)s:'
           '%(lineno)d - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)


def fill_languages():
    logger.info("Filling languages...")
    languages = json_utils.get_languages()
    with connect_to_db() as conn:
        cursor = conn.cursor()
        for lang in languages:
            cursor.execute("""
                        INSERT INTO language (code, description)
                        VALUES (:code, :description)
                    """, lang)
        conn.commit()


def fill_topics():
    logger.info("Filling topics...")
    topics = json_utils.get_topics_json()
    with connect_to_db() as conn:
        cursor = conn.cursor()
        for topic_id, topic_texts in topics.items():
            cursor.execute("""
                        INSERT INTO topic (id, description)
                        VALUES (?, ?)
                    """, (topic_id, topic_texts['ru']))

            cursor.execute('SELECT id, code FROM language')

            # Выводим результаты
            for language_id, language_code in cursor.fetchall():
                cursor.execute("""
                                INSERT INTO topic_translation (topic_id, language_id, text)
                                VALUES (?, ?, ?)
                            """, (topic_id, language_id, topic_texts[language_code]))
        conn.commit()


def fill_categories():
    logger.info("Filling categories...")

    categories = json_utils.get_categories_json()
    with connect_to_db() as conn:
        cursor = conn.cursor()
        for category_id, category in categories.items():
            cursor.execute("""
                        INSERT INTO category (id, code)
                        VALUES (?, ?)
                    """, (category_id, category['code']))

            cursor.execute('SELECT id, code FROM language')

            # Выводим результаты
            for language_id, language_code in cursor.fetchall():
                cursor.execute("""
                                INSERT INTO category_translation (category_id, language_id, text)
                                VALUES (?, ?, ?)
                            """, (category_id, language_id, category[language_code]))
        conn.commit()


def fill_tickets():
    logger.info("Filling tickets...")

    with connect_to_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, code FROM language')
        first_loop_iteration = True
        answer_ids = {}
        for language_id, language_code in cursor.fetchall():
            tickets = parser.get_tickets(language_code)
            for ticket_id, ticket_data in tickets.items():
                for answer_number, answer_text in ticket_data['answers'].items():
                    # Save the answers to the database
                    if first_loop_iteration:
                        cursor.execute("""
                                    INSERT INTO answer (ticket_id, number)
                                    VALUES (?,?)
                                """, (ticket_id, answer_number))
                        answer_ids[f'{ticket_id}_{answer_number}'] = cursor.lastrowid
                        if ticket_data['correct_answer'] == answer_number:
                            correct_answer_id = answer_ids[f'{ticket_id}_{answer_number}']

                    # Save the translations of the answers to the database
                    answer_id = answer_ids[f'{ticket_id}_{answer_number}']
                    cursor.execute("""
                                INSERT INTO answer_translation (answer_id, language_id, text)
                                VALUES (?,?,?)
                            """, (answer_id, language_id, answer_text))

                # Save the question to the database
                if first_loop_iteration:
                    cursor.execute("""
                                        INSERT INTO ticket (id, correct_answer_id, img_source)
                                        VALUES (?, ?, ?)
                                    """, (ticket_id, correct_answer_id, ticket_data['img_source']))

                # Save the translations of the questions to the database
                cursor.execute("""
                                                INSERT INTO ticket_translation (ticket_id, language_id, text)
                                                VALUES (?,?,?)
                                            """, (ticket_id, language_id, answer_text))
            first_loop_iteration = False
        conn.commit()


def fill_ticket_topic_relations():
    """
    :return: void
    """
    logger.info("Filling ticket_topic_relations...")

    ticket_topic_relations = parser.get_ticket_topic_relations()
    with connect_to_db() as conn:
        cursor = conn.cursor()
        for topic_id, ticket_ids in ticket_topic_relations.items():
            for ticket_id in ticket_ids:
                cursor.execute("""
                            INSERT INTO ticket_topic (ticket_id, topic_id)
                            VALUES (?,?)
                        """, (ticket_id, topic_id))
        conn.commit()


def fill_ticket_category_relations():
    """
    :return: void
    """

    logger.info("Filling ticket_category_relations...")

    ticket_category_relations = parser.get_ticket_category_relations()
    with connect_to_db() as conn:
        cursor = conn.cursor()
        for category_id, ticket_ids in ticket_category_relations.items():
            for ticket_id in ticket_ids:
                cursor.execute("""
                            INSERT INTO ticket_category (ticket_id, category_id)
                            VALUES (?,?)
                        """, (ticket_id, category_id))
        conn.commit()


def prepare():
    """
    Prepare before filling the database:
    Once preparation is complete, translate all files in the `json_sources` directory that do not contain a date mark
    in their filenames. After translation, the data from these files will be written to the database.
    :return: void
    """
    json_utils.create_languages_json()
    json_utils.create_topics_json()
    json_utils.create_categories_json()
    json_utils.create_ticket_descriptions_json()


def fill():
    """
    Fill the database with data.
    :return: void
    """
    fill_languages()
    fill_topics()
    fill_categories()
    fill_tickets()
    fill_ticket_topic_relations()
    fill_ticket_category_relations()


if __name__ == '__main__':
    if json_utils.check_files_filled():
        fill()
