import psycopg2 as dbapi2

def initialize_database(app):
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        # ----------- Can Altıniğne - USERS TABLE ----------------------

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

        query = """INSERT INTO USERS (USERNAME, USER_PASSWORD, PROFILE_PIC, COVER_PIC, MAIL_ADDRESS, REGISTER_DATE) VALUES (
                              'saykolover',
                              'notsafe',
                              'https://pbs.twimg.com/profile_images/772712195918618625/bY7jZS80_400x400.jpg',
                              'https://pbs.twimg.com/profile_banners/626892198/1476549918/1500x500',
                              'saykolover@itu.edu.tr',
                              CURRENT_DATE
                    )"""

        cursor.execute(query)

        # -----------------------------------------------------------------

        connection.commit()
