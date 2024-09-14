import sqlite3
from sqlite3 import Connection
# Контекстный менеджер для подключения к базе данных
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

# Определяем корневую директорию проекта
BASE_DIR = Path(__file__).resolve().parent  # Папка database
DB_PATH = BASE_DIR / 'georgianPDD.db'  # Путь к базе данных


def get_connection(db_path: str = DB_PATH) -> Connection:
    """
    Возвращает подключение к базе данных SQLite.

    :param db_path: Путь к файлу базы данных. По умолчанию 'georgianPDD.db'.
    :return: Объект подключения к базе данных SQLite.
    """
    try:
        connection = sqlite3.connect(db_path)
        return connection
    except sqlite3.Error as e:
        print(f"Ошибка при подключении к базе данных: {e}")
        raise


def close_connection(connection: Connection):
    """
    Закрывает подключение к базе данных SQLite.

    :param connection: Объект подключения к базе данных, который нужно закрыть.
    """
    try:
        if connection:
            connection.close()
    except sqlite3.Error as e:
        print(f"Ошибка при закрытии соединения: {e}")
        raise


@contextmanager
def connect_to_db(db_path: str = DB_PATH) -> Generator[Connection, None, None]:
    """
    Контекстный менеджер для подключения к базе данных. Автоматически закрывает соединение после использования.

    :param db_path: Путь к файлу базы данных. По умолчанию 'georgianPDD.db'.
    """
    connection = None
    try:
        connection = get_connection()
        yield connection
    finally:
        if connection:
            close_connection(connection)
