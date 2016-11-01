import psycopg2 as dbapi2
import json
import re
import os


class DatabaseOPS:
    def __init__(self):

        VCAP_SERVICES = os.getenv('VCAP_SERVICES')

        if VCAP_SERVICES is not None:
            self.config = DatabaseOPS.get_elephantsql_dsn(VCAP_SERVICES)
        else:
            self.config = """user='vagrant' password='vagrant'
                                           host='localhost' port=5432 dbname='itucsdb'"""

    @classmethod
    def get_elephantsql_dsn(cls, vcap_services):
        """Returns the data source name for ElephantSQL."""
        parsed = json.loads(vcap_services)
        uri = parsed["elephantsql"][0]["credentials"]["uri"]
        match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
        user, password, host, _, port, dbname = match.groups()
        dsn = """user='{}' password='{}' host='{}' port={}
                 dbname='{}'""".format(user, password, host, port, dbname)
        return dsn

    def create_tables(self):
        with dbapi2.connect(self.config) as connection:
            cursor = connection.cursor()

            # ----------- Can Altinigne - USERS TABLE ----------------------

            query = """CREATE TABLE IF NOT EXISTS USERS (
                          USER_ID SERIAL PRIMARY KEY,
                          USERNAME varchar(20) UNIQUE NOT NULL,
                          USER_PASSWORD varchar(20) NOT NULL,
                          PROFILE_PIC varchar(255) NOT NULL,
                          COVER_PIC varchar(255) NOT NULL,
                          MAIL_ADDRESS varchar(50) NOT NULL,
                          REGISTER_DATE date NOT NULL
                        )"""

            cursor.execute(query)

            # ----------- Tolga Bilbey - KNOTS TABLE ----------------------

            query = """CREATE TABLE IF NOT EXISTS KNOTS(
                        KNOT_ID SERIAL PRIMARY KEY,
                        OWNER_ID INTEGER NOT NULL REFERENCES USERS(USER_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                        KNOT_CONTENT TEXT,
                        LIKE_COUNTER INTEGER DEFAULT 0,
                        REKNOT_COUNTER INTEGER DEFAULT 0,
                        POST_DATE DATE NOT NULL
                    )"""

            cursor.execute(query)

            # ----------- Ozan ATA - LIKE-REKNOT ----------------------

            query = """CREATE TABLE IF NOT EXISTS LIKE_REKNOT(
                        KNOT_ID INTEGER references KNOTS(KNOT_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                        USER_ID INTEGER references USERS(USER_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                        IS_LIKE BOOLEAN
                    )"""

            cursor.execute(query)

            # ----------- ilknur Meray - USER_INTERACTION TABLE ------------------

            query = """CREATE TABLE IF NOT EXISTS USER_INTERACTION(
                        BASE_USER_ID INTEGER REFERENCES USERS(USER_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                        TARGET_USER_ID INTEGER REFERENCES USERS(USER_ID) ON DELETE CASCADE ON UPDATE CASCADE
                    )"""

            cursor.execute(query)

            # ------------Nursah Melis Cinar- MESSAGES TABLE----------------------

            query = """CREATE TABLE IF NOT EXISTS MESSAGES(
                        MESSAGE_ID SERIAL PRIMARY KEY,
                        MESSAGE_CONTENT TEXT,
                        FROM_USER_ID INTEGER REFERENCES USERS(USER_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                        TO_USER_ID INTEGER REFERENCES USERS(USER_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                        MESSAGE_DATE DATE NOT NULL
                    )"""

            cursor.execute(query)

            connection.commit()
            cursor.close()

    def add_knot(self, owner_id, knot_content, likes, reknots, post_date):
        with dbapi2.connect(self.config) as connection:
            cursor = connection.cursor()

            # ----------- Tolga Bilbey - KNOTS TABLE ----------------------

            query = """INSERT INTO KNOTS (OWNER_ID, KNOT_CONTENT, LIKE_COUNTER, REKNOT_COUNTER, POST_DATE) VALUES (
                                          %s, %s, %s, %s, %s
                        )"""
            try:
                cursor.execute(query, (owner_id, knot_content, likes, reknots, post_date))
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    def update_knot(self, owner_id, knot_content, likes, reknots, post_date, knot_id):
        with dbapi2.connect(self.config) as connection:
            cursor = connection.cursor()

            # ----------- Tolga Bilbey - KNOTS TABLE ----------------------

            query = """UPDATE KNOTS SET OWNER_ID=%s, KNOT_CONTENT=%s, LIKE_COUNTER=%s,
                            REKNOT_COUNTER=%s, POST_DATE=%s  WHERE KNOT_ID=%s"""
            try:
                cursor.execute(query, (owner_id, knot_content, likes, reknots, post_date, knot_id))
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    def delete_knot(self, knot_id):
        with dbapi2.connect(self.config) as connection:
            cursor = connection.cursor()

            # ----------- Tolga Bilbey - KNOTS TABLE ----------------------

            query = """DELETE FROM KNOTS WHERE KNOT_ID=%s"""
            try:
                cursor.execute(query, (knot_id,))
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    def select_knots(self, knot_id=None, owner_id=None, knot_content=None, likes=None, reknots=None, post_date=None):
        with dbapi2.connect(self.config) as connection:
            cursor = connection.cursor()

            # ----------- Tolga Bilbey - KNOTS TABLE ----------------------

            query = """SELECT * FROM KNOTS"""
            tup = tuple()

            if knot_id is not None or owner_id is not None or likes is not None \
                    or reknots is not None or post_date is not None or \
                            knot_content is not None:
                query = query + " WHERE "
                if knot_id is not None:
                    query = query + " KNOT_ID=%s"
                    tup = tup + (knot_id,)
                if owner_id is not None:
                    query = query + " OWNER_ID=%s"
                    tup = tup + (owner_id,)
                if likes is not None:
                    query = query + " LIKE_COUNTER=%s"
                    tup = tup + (likes,)
                if reknots is not None:
                    query = query + " REKNOT_COUNTER=%s"
                    tup = tup + (reknots,)
                if post_date is not None:
                    query = query + " POST_DATE=%s"
                    tup = tup + (post_date,)
                if knot_content is not None:
                    query = query + " KNOT_CONTENT LIKE %s"
                    knot_content = '%{}%'.format(knot_content)
                    tup = tup + (knot_content,)
            try:
                cursor.execute(query, tup)
                knots = cursor.fetchall()
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()
            return knots

    def add_relation(self):
        with dbapi2.connect(self.config) as connection:
            cursor = connection.cursor()

            # ----------- Ozan ATA - LIKE_REKNOT TABLE ----------------------

            query = """INSERT INTO LIKE_REKNOT (KNOT_ID, USER_ID, IS_LIKE) VALUES (
                                          1,
                                          1,
                                          TRUE
                        )"""

            try:
                cursor.execute(query)
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    def add_user_interaction(self):
        with dbapi2.connect(self.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - USER_INTERACTION TABLE -----------------------

            query = """INSERT INTO USER_INTERACTION(BASE_USER_ID, TARGET_USER_ID) VALUES(
                                                    1,
                                                    2
                        )"""

            try:
                cursor.execute(query)
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    def add_message(self):
        with dbapi2.connect(self.config) as connection:
            cursor = connection.cursor()

            # -------------------Nursah Melis Cinar - MESSAGES TABLE ----------------------

            query = """INSERT INTO MESSAGES(MESSAGE_CONTENT, FROM_USER_ID, TO_USER_ID, MESSAGE_DATE) VALUES(
                                                   'Thanks for database management systems lecture notes!',
                                                    1,
                                                    2,
                                                    CURRENT_DATE
                        )"""

            try:
                cursor.execute(query)
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()


database = DatabaseOPS()
