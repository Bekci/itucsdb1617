from database import database
import psycopg2 as dbapi2


class Username:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname


class User:
    def __init__(self, id, username, password, profile_picture, cover_picture, mail_address, register_date):
        self.id = id
        self.username = username
        self.password = password
        self.profile_pic = profile_picture
        self.cover_pic = cover_picture
        self.mail_address = mail_address
        self.register_date = register_date


class UserDatabaseOPS:
    @classmethod
    def add_user(cls, username, password, profile_picture, cover_picture, mail_address):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Can Altinigne - USERS TABLE ----------------------

            query = """INSERT INTO USERS (USERNAME, USER_PASSWORD, PROFILE_PIC, COVER_PIC, MAIL_ADDRESS, REGISTER_DATE) VALUES (
                                              %s,
                                              %s,
                                              %s,
                                              %s,
                                              %s,
                                              CURRENT_DATE
                            )"""

            try:
                cursor.execute(query, (username, password, profile_picture, cover_picture, mail_address))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def update_user(cls, username, password, profile_picture, cover_picture, mail_address):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Can Altinigne - USERS TABLE ----------------------

            query = """UPDATE USERS SET USER_PASSWORD=%s, PROFILE_PIC=%s,
                          COVER_PIC=%s, MAIL_ADDRESS=%s WHERE USERNAME=%s
                            """

            try:
                cursor.execute(query, (password, profile_picture, cover_picture, mail_address, username))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def delete_user(cls, username):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Can Altinigne - USERS TABLE ----------------------

            query = """DELETE FROM USERS WHERE USERNAME = %s"""

            try:
                cursor.execute(query, (username,))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def select_user(cls, username):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Can Altinigne - USERS TABLE ----------------------

            query = """SELECT * FROM USERS WHERE USERNAME=%s"""

            try:
                cursor.execute(query, (username,))
                user_data = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            if user_data:
                return User(id=user_data[0], username=user_data[1], password=user_data[2], profile_picture=user_data[3],
                            cover_picture=user_data[4],
                            mail_address=user_data[5], register_date=user_data[6])
            else:
                return -1

    @classmethod
    def select_users_for_search(cls, username):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Can Altinigne - USERS TABLE ----------------------

            str = "%{}%".format(username)

            query = """SELECT * FROM USERS WHERE USERNAME LIKE %s"""

            user_data = []

            try:
                cursor.execute(query, (str,))
                user_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            user_list = []

            for row in user_data:
                user_list.append(
                    User(id=row[0], username=row[1], password=row[2], profile_picture=row[3], cover_picture=row[4],
                         mail_address=row[5], register_date=row[6]))

            return user_list

    @classmethod
    def select_user_with_id(cls, user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Can Altinigne - USERS TABLE ----------------------

            query = """SELECT * FROM USERS WHERE USER_ID=%s"""

            try:
                cursor.execute(query, (user_id,))
                user_data = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            if user_data:
                return User(id=user_data[0], username=user_data[1], password=user_data[2], profile_picture=user_data[3],
                            cover_picture=user_data[4],
                            mail_address=user_data[5], register_date=user_data[6])
            else:
                return -1

    @classmethod
    def select_user_name_surname(cls, username):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Can Altinigne - USERS TABLE ----------------------

            query = """SELECT * FROM USERS_NAMES WHERE USERNAME=%s"""
            user_data = 0

            try:
                cursor.execute(query, (username,))
                user_data = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            if user_data and user_data != 0:
                return Username(user_data[1], user_data[2])
            else:
                return -1

    @classmethod
    def add_real_name(cls, username, real_name, real_surname):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Can Altinigne - USERS TABLE ----------------------

            query = """INSERT INTO USERS_NAMES (USERNAME, U_NAME, U_SURNAME) VALUES (
                                                  %s,
                                                  %s,
                                                  %s
                                )"""

            try:
                cursor.execute(query, (username, real_name, real_surname))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def update_real_name(cls, username, real_name, real_surname):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Can Altinigne - USERS TABLE ----------------------

            query = """UPDATE USERS_NAMES SET U_NAME=%s, U_SURNAME=%s
                              WHERE USERNAME=%s
                                """

            try:
                cursor.execute(query, (real_name, real_surname, username))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def delete_real_name(cls, username):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Can Altinigne - USERS TABLE ----------------------

            query = """DELETE FROM USERS_NAMES WHERE USERNAME = %s"""

            try:
                cursor.execute(query, (username,))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()


user_ops = UserDatabaseOPS()
