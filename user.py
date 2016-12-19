from database import database
from flask_login import UserMixin
import psycopg2 as dbapi2


class UserDetails:
    def __init__(self, username, name, surname, city, country):
        self.username = username
        self.name = name
        self.surname = surname
        self.city = city
        self.country = country


class User(UserMixin):
    def __init__(self, id, username, password, profile_picture, cover_picture, mail_address, register_date):
        self.id = id
        self.username = username
        self.password = password
        self.profile_pic = profile_picture
        self.cover_pic = cover_picture
        self.mail_address = mail_address
        self.register_date = register_date

        
class SearchedUser:
    def __init__(self, id, username, follower_number, following_number, profile_picture, cover_picture, maybe_i_am):
        self.id = id
        self.username = username
        self.follower_number = follower_number
        self.following_number = following_number
        self.profile_picture = profile_picture
        self.cover_picture = cover_picture
        self.are_you_following_me = maybe_i_am


class FollowerOrFollwingUser:
    def __init__(self, username, profile_pic, user_id):
        self.username = username
        self.profile_pic = profile_pic
        self.id = user_id


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

            user_data = None

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
    def select_users_for_search(cls, username, current_user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Can Altinigne - USERS TABLE ----------------------

            str = "%{}%".format(username)

            query = """SELECT USERS.USER_ID, USERS.USERNAME, USERS.COVER_PIC, USERS.PROFILE_PIC, COUNT(USER_INTERACTION.BASE_USER_ID) FROM USERS
                       INNER JOIN USER_DETAIL ON USERS.USERNAME=USER_DETAIL.USERNAME
                       LEFT JOIN USER_INTERACTION ON USERS.USER_ID=USER_INTERACTION.BASE_USER_ID
                       WHERE USERS.USERNAME LIKE %s
                       GROUP BY USERS.USER_ID, USERS.USERNAME, USERS.COVER_PIC, USERS.PROFILE_PIC, USER_INTERACTION.BASE_USER_ID
                       ORDER BY USERS.USER_ID
                    """

            user_data = []

            try:
                cursor.execute(query, (str,))
                user_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            query = """SELECT COUNT(USER_INTERACTION.TARGET_USER_ID) FROM USERS
                       LEFT JOIN USER_INTERACTION ON USERS.USER_ID=USER_INTERACTION.TARGET_USER_ID
                       WHERE USERS.USERNAME LIKE %s
                       GROUP BY USERS.USERNAME, USER_INTERACTION.TARGET_USER_ID, USERS.USER_ID
                       ORDER BY USERS.USER_ID
                                """

            user_follower_number = []
            followers = []

            try:
                cursor.execute(query, (str,))
                user_follower_number = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            for row in user_follower_number:
                followers.append(row[0])

            query = """SELECT USERS.USER_ID FROM USERS
                       INNER JOIN USER_INTERACTION ON USERS.USER_ID=USER_INTERACTION.TARGET_USER_ID
                       WHERE USER_INTERACTION.BASE_USER_ID=%s AND (USERS.USERNAME LIKE %s)
                    """

            people_that_i_follow = []
            i_followed = []           

            try:
                cursor.execute(query, (current_user_id, str))
                people_that_i_follow = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            for row in people_that_i_follow:
                i_followed.append(row[0])

            cursor.close()

            user_list = []
            i = 0

            for row in user_data:

                i_am_following = row[0] in i_followed

                user_list.append(
                    SearchedUser(id=row[0], username=row[1], follower_number=followers[i],
                                 following_number=row[4], profile_picture=row[3],
                                 cover_picture=row[2], maybe_i_am=i_am_following
                                 )
                )

                i+=1

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
    def get_followers(cls, user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Can Yilmaz Altinigne - USERS TABLE ----------------------

            query = """SELECT USERS.PROFILE_PIC, USERS.USERNAME, USERS.USER_ID FROM USER_INTERACTION
                       INNER JOIN USERS ON USERS.USER_ID=USER_INTERACTION.BASE_USER_ID
                       WHERE USER_INTERACTION.TARGET_USER_ID = %s
                    """
            user_list = []
            try:
                cursor.execute(query, (user_id,))
                user_list = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            follower = []

            for row in user_list:
                follower.append(
                    FollowerOrFollwingUser(username=row[1], profile_pic=row[0], user_id=row[2])
                )

            return follower

    @classmethod
    def get_following(cls, user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Can Yilmaz Altinigne - USERS TABLE ----------------------

            query = """SELECT USERS.PROFILE_PIC, USERS.USERNAME, USERS.USER_ID  FROM USER_INTERACTION
                       INNER JOIN USERS ON USERS.USER_ID=USER_INTERACTION.TARGET_USER_ID
                       WHERE USER_INTERACTION.BASE_USER_ID = %s
                                """
            user_list = []
            try:
                cursor.execute(query, (user_id,))
                user_list = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            following = []

            for row in user_list:

                following.append(
                    FollowerOrFollwingUser(username=row[1], profile_pic=row[0], user_id=row[2])
                )

            return following

    @classmethod
    def get_random_users(cls, user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Can Yilmaz Altinigne - USERS TABLE ----------------------

            query = """ SELECT DISTINCT USERS.PROFILE_PIC, USERS.USERNAME, USERS.USER_ID  FROM USERS, USER_INTERACTION
                        WHERE USER_ID != %s AND USER_ID NOT IN (SELECT TARGET_USER_ID FROM USER_INTERACTION
                       INNER JOIN USERS ON USERS.USER_ID=USER_INTERACTION.TARGET_USER_ID
                       WHERE USER_INTERACTION.BASE_USER_ID = %s)
                       LIMIT 3
                                    """
            user_list = []
            try:
                cursor.execute(query, (user_id, user_id))
                user_list = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            following = []

            for row in user_list:
                following.append(
                    FollowerOrFollwingUser(username=row[1], profile_pic=row[0], user_id=row[2])
                )

            return following

    @classmethod
    def select_user_detail(cls, username):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Can Altinigne - USERS TABLE ----------------------

            query = """SELECT USER_DETAIL.*, CITIES.CITY_NAME, CITIES.COUNTRY FROM USER_DETAIL
                       INNER JOIN USERS ON USERS.USERNAME=USER_DETAIL.USERNAME
                       INNER JOIN CITIES ON CITIES.CITY_ID=USER_DETAIL.CITY_ID
                       WHERE USER_DETAIL.USERNAME=%s"""
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
                return UserDetails(username=user_data[0], name=user_data[1], surname=user_data[2],
                                   city=user_data[4], country=user_data[5])
            else:
                return -1

    @classmethod
    def add_user_detail(cls, username, real_name, real_surname, city_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Can Altinigne - USERS TABLE ----------------------

            query = """INSERT INTO USER_DETAIL (USERNAME, U_NAME, U_SURNAME, CITY_ID) VALUES (
                                                  %s,
                                                  %s,
                                                  %s,
                                                  %s
                                )"""

            try:
                cursor.execute(query, (username, real_name, real_surname, city_id))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def update_user_detail(cls, username, real_name, real_surname, city_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Can Altinigne - USERS TABLE ----------------------

            query = """UPDATE USER_DETAIL SET U_NAME=%s, U_SURNAME=%s, CITY_ID=%s
                              WHERE USERNAME=%s
                                """

            try:
                cursor.execute(query, (real_name, real_surname, city_id, username))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def delete_user_detail(cls, username):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Can Altinigne - USERS TABLE ----------------------

            query = """DELETE FROM USER_DETAIL WHERE USERNAME = %s"""

            try:
                cursor.execute(query, (username,))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def follow(cls, user_id, target_user):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Ozan ATA - USERS TABLE ----------------------

            query = """INSERT INTO user_interaction (base_user_id, target_user_id)
                        VALUES (%s, %s)
                            """

            try:
                cursor.execute(query, (user_id, target_user))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def unfollow(cls, user_id, target_user):
       with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Ozan ATA - USERS TABLE ----------------------

            query = """delete from user_interaction
                            where 
                        base_user_id = %s
                        and target_user_id = %s
                            """

            try:
                cursor.execute(query, (user_id, target_user))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

user_ops = UserDatabaseOPS()
