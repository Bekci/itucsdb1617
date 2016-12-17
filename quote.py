from database import database
import psycopg2 as dbapi2


class Quote:
    def __init__(self, book_name, quote_id, quote_content, quoted_book_id, quote_user_id):
        self.book_name = book_name
        self.quote_id = quote_id
        self.quote_content = quote_content
        self.quoted_book_id = quoted_book_id
        self.quote_user_id = quote_user_id


class QuoteDatabaseOPS:
    @classmethod
    def add_quote(cls, quote_content, quoted_book_id, quote_user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            # ----------- ilknur Meray - QUOTE TABLE -----------------------

            query = """INSERT INTO QUOTE (QUOTE_CONTENT, QUOTED_BOOK_ID, QUOTE_USER_ID) VALUES (
                                                %s,
                                                %s,
                                                %s
                        )"""

            try:
                cursor.execute(query, (quote_content, quoted_book_id, quote_user_id))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def update_quote(cls, quote_id, new_quote_content, new_quoted_book):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - QUOTE TABLE -----------------------

            query = """UPDATE QUOTE SET QUOTE_CONTENT = %s,
                                        QUOTED_BOOK_ID = %s WHERE QUOTE_ID = %s"""

            try:
                cursor.execute(query, (new_quote_content, new_quoted_book, quote_id))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def delete_quote(cls, quote_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - QUOTE TABLE -----------------------

            query = """DELETE FROM QUOTE WHERE QUOTE_ID = %s"""

            try:
                cursor.execute(query, (quote_id,))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def select_quotes(cls, quote_user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - QUOTE TABLE -----------------------

            query = """SELECT q.QUOTE_ID, q.QUOTE_CONTENT, q.QUOTED_BOOK_ID, q.QUOTE_USER_ID, b.BOOK_TITLE
                        FROM QUOTE AS q LEFT JOIN BOOK AS b ON q.QUOTED_BOOK_ID = b.BOOK_ID WHERE q.QUOTE_USER_ID = %s"""

            quote_data = []
            try:
                cursor.execute(query, (quote_user_id,))
                quote_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            quote_list = []

            for element in quote_data:
                quote_list.append(
                    Quote(quote_id=element[0], quote_content=element[1], quoted_book_id=element[2], quote_user_id=element[3], book_name=element[4]))

            return quote_list

book_quote_ops = QuoteDatabaseOPS()
