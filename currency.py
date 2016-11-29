from database import database
import psycopg2 as dbapi2


class Currency:
    def __init__(self, name, to_tl, date):
        self.name = name
        self.tl_value = to_tl
        self.last_update = date


class CurrencyDatabaseOPS:
    @classmethod
    def add_currency(cls, name, to_tl):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO CURRENCIES (CURRENCY_NAME, CURRENCY_TO_TL, LAST_UPDATE) VALUES (
                                              %s,
                                              %s,
                                              CURRENT_DATE
                            )"""

            try:
                cursor.execute(query, (name, to_tl))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def delete_currency(cls, name):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM CURRENCIES WHERE CURRENCY_NAME = %s"""

            try:
                cursor.execute(query, (name,))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def update_currency(cls, name, new_currency):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """UPDATE CURRENCIES SET LAST_UPDATE=CURRENT_DATE , CURRENCY_TO_TL=%s
                        WHERE CURRENCY_NAME=%s
                                """

            try:
                cursor.execute(query, (new_currency, name))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def select_currency(cls, name):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM CURRENCIES WHERE CURRENCY_NAME = %s"""

            try:
                cursor.execute(query, (name,))
                currency_data = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            if currency_data:
                return Currency(name=currency_data[0], to_tl=currency_data[1], date=currency_data[2])
            else:
                return -1

    @classmethod
    def select_all_currencies(cls):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM CURRENCIES"""

            currency_data = []

            try:
                cursor.execute(query, ())
                currency_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            user_list = []

            for row in currency_data:
                user_list.append(
                    Currency(name=row[0], to_tl=row[1], date=row[2])
                )

            return user_list


currency_ops = CurrencyDatabaseOPS()
