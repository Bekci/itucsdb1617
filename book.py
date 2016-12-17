from database import database
import psycopg2 as dbapi2
from shelf import ShelfDatabaseOPS


class Book:
    def __init__(self, book_id, book_title, book_cover, book_writer, book_genre, date_read, user_rate, book_review, book_shelf, book_reader_id):
        self.book_id = book_id
        self.book_title = book_title
        self.book_cover = book_cover
        self.book_writer = book_writer
        self.book_genre = book_genre
        self.date_read = date_read
        self.user_rate = user_rate
        self.book_review = book_review
        self.book_shelf = book_shelf
        self.book_reader_id = book_reader_id


class BookDatabaseOPS:
    @classmethod
    def add_book(cls, book_title, book_cover, book_writer, book_genre, date_read, user_rate, book_review, book_shelf, book_reader_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - BOOK TABLE -----------------------

            query = """INSERT INTO BOOK (BOOK_TITLE, BOOK_COVER, BOOK_WRITER, BOOK_GENRE, DATE_READ, USER_RATE, BOOK_REVIEW, BOOK_SHELF_ID, BOOK_READER_ID) VALUES (
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s
                        )"""

            try:
                cursor.execute(query, (book_title, book_cover, book_writer, book_genre, date_read, user_rate, book_review, book_shelf, book_reader_id))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()
            ShelfDatabaseOPS.increase_book_counter(book_shelf)

    @classmethod
    def update_book(cls, book_id, book_title, book_cover, book_writer, book_genre, date_read, user_rate, book_review, book_shelf, book_reader_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - BOOK TABLE -----------------------

            query = """UPDATE BOOK SET BOOK_TITLE=%s,
                                    BOOK_COVER = %s,
                                    BOOK_WRITER = %s,
                                    BOOK_GENRE = %s,
                                    DATE_READ = %s,
                                    USER_RATE = %s,
                                    BOOK_REVIEW = %s,
                                    BOOK_SHELF_ID = %s WHERE BOOK_ID = %s AND BOOK_READER_ID = %s"""

            try:
                cursor.execute(query, (book_title, book_cover, book_writer, book_genre, date_read, user_rate, book_review, book_shelf, book_id, book_reader_id))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def find_shelf_from_id(cls, book_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - BOOK TABLE -----------------------

            query = """SELECT BOOK_SHELF_ID FROM BOOK WHERE BOOK_ID=%s"""

            try:
                cursor.execute(query, (book_id,))
                book_data = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            return book_data

    @classmethod
    def delete_book(cls, book_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - BOOK TABLE -----------------------

            query = """DELETE FROM BOOK WHERE BOOK_ID = %s"""

            try:
                cursor.execute(query, (book_id,))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def select_all_books_of_user(cls, book_reader_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - BOOK TABLE -----------------------

            query = """SELECT * FROM BOOK WHERE BOOK_READER_ID=%s ORDER BY USER_RATE DESC"""

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
                    Book(book_id=element[0], book_title=element[1], book_cover=element[2], book_writer=element[3], book_genre=element[4],
                         date_read=element[5], user_rate=element[6], book_review=element[7], book_shelf=element[8], book_reader_id=element[9]))

            return book_list

    @classmethod
    def select_books_from_shelf(cls, book_shelf, book_reader_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - BOOK TABLE -----------------------
            query = """SELECT * FROM BOOK WHERE BOOK_SHELF_ID=%s AND BOOK_READER_ID = %s"""

            book_data = []

            try:
                cursor.execute(query, (book_shelf, book_reader_id))
                book_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            book_list = []

            for element in book_data:
                book_list.append(
                    Book(book_id=element[0], book_title=element[1], book_cover=element[2], book_writer=element[3], book_genre=element[4],
                         date_read=element[5], user_rate=element[6], book_review=element[7], book_shelf=element[8], book_reader_id=element[9]))

            return book_list


book_ops = BookDatabaseOPS()
