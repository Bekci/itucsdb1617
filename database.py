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

            # ----------- Can Altiniğne - USERS TABLE ----------------------

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

            # -----------------------------------------------------------------
            #           CREATE TABLE COMMANDS WILL BE HERE

            # -----------------------------------------------------------------

            connection.commit()
            cursor.close()

    def add_user(self):
        with dbapi2.connect(self.config) as connection:
            cursor = connection.cursor()

            # ----------- Can Altıniğne - USERS TABLE ----------------------

            query = """INSERT INTO USERS (USERNAME, USER_PASSWORD, PROFILE_PIC, COVER_PIC, MAIL_ADDRESS, REGISTER_DATE) VALUES (
                                          'osman',
                                          'notsafe',
                                          'https://pbs.twimg.com/profile_images/772712195918618625/bY7jZS80_400x400.jpg',
                                          'https://pbs.twimg.com/profile_banners/626892198/1476549918/1500x500',
                                          'saykolover@itu.edu.tr',
                                          CURRENT_DATE
                        )"""

            try:
                cursor.execute(query)
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    def add_knot(self):
        with dbapi2.connect(self.config) as connection:
            cursor = connection.cursor()

            # ----------- Tolga Bilbey - KNOTS TABLE ----------------------

            query = """INSERT INTO KNOTS (OWNER_ID, KNOT_CONTENT, LIKE_COUNTER, REKNOT_COUNTER, POST_DATE) VALUES (
                                          1,
                                          'First content of the Knitter',
                                          0,
                                          0,
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
