from database import database
import psycopg2 as dbapi2


class Shelf:
    def __init__(self, shelf_id, shelf_name, is_main, book_counter, shelf_user_id):
        self.shelf_id = shelf_id
        self.shelf_name = shelf_name
        self.is_main = is_main
        self.book_counter = book_counter
        self.shelf_user_id = shelf_user_id


class ShelfDatabaseOPS:
    @classmethod
    def add_shelf(cls, shelf_name, is_main, shelf_user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            book_counter = 0
            # ----------- ilknur Meray - SHELF TABLE -----------------------

            query = """INSERT INTO SHELF (SHELF_NAME, IS_MAIN, BOOK_COUNTER, SHELF_USER_ID) VALUES (
                                                %s,
                                                %s,
                                                %s,
                                                %s
                        )"""

            try:
                cursor.execute(query, (shelf_name, is_main, book_counter, shelf_user_id))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def update_shelf_name(cls, shelf_id, new_shelf_name):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - SHELF TABLE -----------------------

            query = """UPDATE SHELF SET SHELF_NAME = %s WHERE SHELF_ID = %s"""

            try:
                cursor.execute(query, (new_shelf_name, shelf_id))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def update_main_shelf(cls, shelf_id, is_main):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - SHELF TABLE -----------------------
            if is_main:
                query = """UPDATE SHELF SET IS_MAIN = %s WHERE SHELF_ID = %s"""

                try:
                    cursor.execute(query, (is_main, shelf_id,))
                except dbapi2.Error:
                    connection.rollback()
                else:
                    connection.commit()

                cursor.close()

                cursor = connection.cursor()
                query = """UPDATE SHELF SET IS_MAIN = FALSE WHERE SHELF_ID <> %s"""

                try:
                    cursor.execute(query, (shelf_id,))
                except dbapi2.Error:
                    connection.rollback()
                else:
                    connection.commit()

                cursor.close()
            else:
                query = """UPDATE SHELF SET IS_MAIN = %s WHERE SHELF_ID = %s"""

                try:
                    cursor.execute(query, (is_main, shelf_id,))
                except dbapi2.Error:
                    connection.rollback()
                else:
                    connection.commit()

                cursor.close()

                cursor = connection.cursor()
                query = """UPDATE SHELF SET IS_MAIN = TRUE WHERE SHELF_ID <> %s"""

                try:
                    cursor.execute(query, (shelf_id,))
                except dbapi2.Error:
                    connection.rollback()
                else:
                    connection.commit()

                cursor.close()

    @classmethod
    def delete_shelf(cls, shelf_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - SHELF TABLE -----------------------

            query = """DELETE FROM SHELF WHERE SHELF_ID = %s"""

            try:
                cursor.execute(query, (shelf_id,))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def select_shelves(cls, shelf_user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - SHELF TABLE -----------------------

            query = """SELECT * FROM SHELF WHERE SHELF_USER_ID = %s"""

            shelf_data = []
            try:
                cursor.execute(query, (shelf_user_id,))
                shelf_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            shelf_list = []

            for element in shelf_data:
                shelf_list.append(
                    Shelf(shelf_id=element[0], shelf_name=element[1], is_main=element[2], book_counter=element[3], shelf_user_id=element[4]))

            for j in shelf_list:
                if j.is_main:
                    a, b = shelf_list.index(j), 0
                    shelf_list[b], shelf_list[a] = shelf_list[a], shelf_list[b]

            return shelf_list

    @classmethod
    def increase_book_counter(cls, shelf_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - SHELF TABLE -----------------------

            query = """UPDATE SHELF SET BOOK_COUNTER = BOOK_COUNTER+1 WHERE SHELF_ID = %s"""

            try:
                cursor.execute(query, (shelf_id,))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def decrease_book_counter(cls, shelf_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - SHELF TABLE -----------------------

            query = """UPDATE SHELF SET BOOK_COUNTER = BOOK_COUNTER-1 WHERE SHELF_ID = %s"""

            try:
                cursor.execute(query, (shelf_id,))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

book_shelf_ops = ShelfDatabaseOPS()
