from database.connection import connect_to_db


def create_tables():
    with connect_to_db() as conn:
        with open('install.sql', 'r') as sql_file:
            sql_script = sql_file.read()

        cursor = conn.cursor()
        cursor.executescript(sql_script)
        conn.commit()


if __name__ == "__main__":
    create_tables()
