from database import database
import psycopg2 as dbapi2
from book_type import BookTypeDatabaseOPS

class Book:
    def __init__(self, book_id, book_title, book_cover, book_writer, date_read, book_review, book_type_id, book_reader_id):
        self.book_id = book_id
        self.book_title = book_title
        self.book_cover = book_cover
        self.book_writer = book_writer
        self.date_read = date_read
        self.book_review = book_review
        self.book_type_id = book_type_id
        self.book_reader_id = book_reader_id


class BookDatabaseOPS:
    @classmethod
    def add_book(cls, book_title, book_cover, book_writer, date_read, book_review, book_type_name, book_reader_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - BOOK TABLE -----------------------

            type_info = BookTypeDatabaseOPS.select_book_type_with_name(book_type_name)
            query = """INSERT INTO BOOK (BOOK_TITLE, BOOK_COVER, BOOK_WRITER, DATE_READ, BOOK_REVIEW, BOOK_TYPE_ID, BOOK_READER_ID) VALUES (
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                        )"""

            try:
                cursor.execute(query, (book_title, book_cover, book_writer, date_read, book_review, type_info, book_reader_id))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def update_book(cls, book_id, book_title, book_cover, book_writer, date_read, book_review, book_type_name, book_reader_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - BOOK TABLE -----------------------

            type_info = BookTypeDatabaseOPS.select_book_type_with_name(book_type_name)
            query = """UPDATE BOOK SET BOOK_TITLE=%s,
                                    BOOK_COVER=%s,
                                    BOOK_WRITER=%s,
                                    DATE_READ=%s,
                                    BOOK_REVIEW=%s,
                                    BOOK_TYPE_ID=%s WHERE BOOK_ID=%s AND BOOK_READER_ID=%s"""

            try:
                cursor.execute(query, (book_title, book_cover, book_writer, date_read, book_review, type_info, book_id, book_reader_id))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def delete_book(cls, book_id, book_reader_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - BOOK TABLE -----------------------

            query = """DELETE FROM BOOK WHERE BOOK_ID = %s AND BOOK_READER_ID=%s"""

            try:
                cursor.execute(query, (book_id, book_reader_id))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def select_all_books(cls, book_reader_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - BOOK TABLE -----------------------

            query = """SELECT * FROM BOOK WHERE BOOK_READER_ID=%s"""

            book_data = []

            try:
                cursor.execute(query, (book_reader_id,))
                book_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            book_list = []

            for element in book_data:
                book_list.append(
                    Book(book_id=element[0], book_title=element[1], book_cover=element[2], book_writer=element[3], date_read=element[4],
                         book_review=element[5], book_type_id=element[6], book_reader_id=element[7]))

            return book_list

    @classmethod
    def select_books_with_type(cls, book_type_name):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - BOOK TABLE -----------------------
            type_info = BookTypeDatabaseOPS.select_book_type_with_name(book_type_name)
            query = """SELECT * FROM BOOK WHERE BOOK_TYPE_ID=%s"""

            book_data = []

            try:
                cursor.execute(query, (type_info[0],))
                book_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            book_list = []

            for element in book_data:
                book_list.append(
                    Book(book_id=element[0], book_title=element[1], book_cover=element[2], book_writer=element[3], date_read=element[4],
                         book_review=element[5], book_type_id=element[6], book_reader_id=element[7]))

            return book_list


book_ops = BookDatabaseOPS()
