from database import database
import psycopg2 as dbapi2


class BookType:
    def __init__(self, type_id, type_name, type_counter):
        self.type_id = type_id
        self.type_name = type_name
        self.type_counter = type_counter


class BookTypeDatabaseOPS:
    @classmethod
    def add_book_type(cls, type_name):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            type_counter = 1
            # ----------- ilknur Meray - BOOK_TYPE TABLE -----------------------

            query = """INSERT INTO BOOK_TYPE (TYPE_NAME, TYPE_COUNTER) VALUES (
                                                %s,
                                                %s
                        )"""

            try:
                cursor.execute(query, (type_name, type_counter))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def update_book_type_name(cls, new_type_name, old_type_name):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - BOOK_TYPE TABLE -----------------------

            query = """UPDATE BOOK_TYPE SET TYPE_NAME = %s WHERE TYPE_NAME = %s"""

            try:
                cursor.execute(query, (new_type_name, old_type_name))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def delete_book_type(cls, type_name):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - BOOK_TYPE TABLE -----------------------

            query = """DELETE FROM BOOK_TYPE WHERE TYPE_NAME = %s"""

            try:
                cursor.execute(query, (type_name,))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def select_book_type_with_name(cls, type_name):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - BOOK_TYPE TABLE -----------------------

            query = """SELECT * FROM BOOK_TYPE WHERE TYPE_NAME = %s"""

            try:
                cursor.execute(query, (type_name,))
                type_data = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            return BookType(type_id=type_data[0], type_name=type_data[1], type_counter=type_data[2])

    @classmethod
    def select_book_type_with_id(cls, type_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - BOOK_TYPE TABLE -----------------------

            query = """SELECT * FROM BOOK_TYPE WHERE TYPE_ID = %s"""

            try:
                cursor.execute(query, (type_id,))
                type_data1 = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            return BookType(type_id=type_data1[0], type_name=type_data1[1], type_counter=type_data1[2])

    @classmethod
    def increase_type_counter(cls, type_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - BOOK_TYPE TABLE -----------------------

            query = """UPDATE BOOK_TYPE SET TYPE_COUNTER = TYPE_COUNTER+1 WHERE TYPE_ID = %s"""

            try:
                cursor.execute(query, (type_id,))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def decrease_type_counter(cls, type_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - BOOK_TYPE TABLE -----------------------

            query = """UPDATE BOOK_TYPE SET TYPE_COUNTER = TYPE_COUNTER-1 WHERE TYPE_ID = %s"""

            try:
                cursor.execute(query, (type_id,))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

book_type_ops = BookTypeDatabaseOPS()
