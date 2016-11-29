from database import database
import psycopg2 as dbapi2


class SellerInformation:
    def __init__(self, username, profile_pic, mail_address):
        self.username = username
        self.profile_pic = profile_pic
        self.mail_address = mail_address


class ItemInformation:
    def __init__(self, item_id, item_name, item_picture, item_price, item_description, item_currency, item_city, item_country):
        self.item_id = item_id
        self.item_name = item_name
        self.item_picture = item_picture
        self.item_price = item_price
        self.item_description = item_description
        self.item_currency = item_currency
        self.item_city = item_city
        self.item_country = item_country


class Sale:
    def __init__(self, seller_information, sale_id, sale_start, sale_end, item_info):
        self.sale_id = sale_id
        self.sale_start = sale_start
        self.sale_end = sale_end
        self.seller = seller_information
        self.item = item_info


class SaleDatabaseOPS:
    @classmethod
    def add_sale(cls, seller_id, item_id, city_id, end_date):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO SALES (SELLER_ID, ITEM_ID, CITY_ID, START_DATE, END_DATE) VALUES (
                                              %s,
                                              %s,
                                              %s,
                                              CURRENT_DATE,
                                              %s
                            )"""

            try:
                cursor.execute(query, (seller_id, item_id, city_id, end_date))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def add_item(cls, item_name, item_picture, item_price, item_description, item_currency):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()


            query = """INSERT INTO ITEMS (ITEM_NAME, ITEM_PICTURE, ITEM_PRICE, ITEM_DESCRIPTION, ITEM_CURRENCY) VALUES (
                                              %s,
                                              %s,
                                              %s,
                                              %s,
                                              %s
                            )"""

            try:
                cursor.execute(query, (item_name, item_picture, item_price, item_description, item_currency))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def select_new_item_id(cls, item_name, item_picture, item_price):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()


            query = """SELECT ITEM_ID FROM ITEMS WHERE ITEM_NAME=%s and ITEM_PICTURE=%s and ITEM_PRICE=%s"""

            user_data = None

            try:
                cursor.execute(query, (item_name, item_picture, item_price))
                user_data = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            if user_data:
                return user_data[0]
            else:
                return -1

    @classmethod
    def update_sale(cls, description, end_date, city_id, sale_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """UPDATE SALES SET END_DATE=%s, CITY_ID=%s
                        WHERE SALE_ID=%s"""

            try:
                cursor.execute(query, (description, end_date, city_id, sale_id))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def delete_sale(cls, sale_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM SALES WHERE SALE_ID = %s"""

            try:
                cursor.execute(query, (sale_id,))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def select_sales_of_a_user(cls, username):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT s.SALE_ID, u.USERNAME, u.PROFILE_PIC, u.MAIL_ADDRESS, s.START_DATE, s.END_DATE, i.*, CITIES.CITY_NAME, CITIES.COUNTRY
                       FROM USERS AS u
                       INNER JOIN SALES AS s ON s.SELLER_ID=u.USER_ID
                       INNER JOIN ITEMS AS i ON s.ITEM_ID=i.ITEM_ID
                       INNER JOIN CURRENCIES AS c ON i.ITEM_CURRENCY=c.CURRENCY_NAME
                       INNER JOIN CITIES ON s.CITY_ID=CITIES.CITY_ID
                       WHERE u.USERNAME=%s"""

            user_data = []

            try:
                cursor.execute(query, (username,))
                user_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            sale_list = []

            for row in user_data:
                sale_list.append(
                    Sale(SellerInformation(username=row[1], profile_pic=row[2], mail_address=row[3]), sale_id=row[0],
                         sale_start=row[4], sale_end=row[5], item_info=ItemInformation(item_id=row[6],
                                                                                       item_name=row[7],
                                                                                       item_picture=row[8],
                                                                                       item_price=row[9],
                                                                                       item_description=row[10],
                                                                                       item_currency=row[11],
                                                                                       item_city=row[12],
                                                                                       item_country=row[13]
                                                                                       )
                         )
                )

            return sale_list

    @classmethod
    def select_newest_items(cls, username):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT s.SALE_ID, u.USERNAME, u.PROFILE_PIC, u.MAIL_ADDRESS, s.START_DATE, s.END_DATE, i.*, CITIES.CITY_NAME, CITIES.COUNTRY FROM USERS AS u
                           INNER JOIN SALES AS s ON s.SELLER_ID=u.USER_ID
                           INNER JOIN ITEMS AS i ON s.ITEM_ID=i.ITEM_ID
                           INNER JOIN CURRENCIES AS c ON i.ITEM_CURRENCY=c.CURRENCY_NAME
                           INNER JOIN CITIES ON s.CITY_ID=CITIES.CITY_ID
                           WHERE u.USERNAME<>%s
                           ORDER BY current_date-s.START_DATE
                           LIMIT 10"""

            user_data = []

            try:
                cursor.execute(query, (username,))
                user_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            sale_list = []

            for row in user_data:
                sale_list.append(
                    Sale(SellerInformation(username=row[1], profile_pic=row[2], mail_address=row[3]), sale_id=row[0],
                         sale_start=row[4], sale_end=row[5], item_info=ItemInformation(item_id=row[6],
                                                                                       item_name=row[7],
                                                                                       item_picture=row[8],
                                                                                       item_price=row[9],
                                                                                       item_description=row[10],
                                                                                       item_currency=row[11],
                                                                                       item_city=row[12],
                                                                                       item_country=row[13]
                                                                                       )
                         )
                )

            return sale_list

    @classmethod
    def select_items_by_currency(cls, currency, username):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT s.SALE_ID, u.USERNAME, u.PROFILE_PIC, u.MAIL_ADDRESS, s.START_DATE, s.END_DATE, i.*, CITIES.CITY_NAME, CITIES.COUNTRY FROM USERS AS u
                               INNER JOIN SALES AS s ON s.SELLER_ID=u.USER_ID
                               INNER JOIN ITEMS AS i ON s.ITEM_ID=i.ITEM_ID
                               INNER JOIN CURRENCIES AS c ON i.ITEM_CURRENCY=c.CURRENCY_NAME
                               INNER JOIN CITIES ON s.CITY_ID=CITIES.CITY_ID
                               WHERE c.CURRENCIES=%s AND u.USERNAME<>%s
                               """

            user_data = []

            try:
                cursor.execute(query, (currency, username))
                user_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            sale_list = []

            for row in user_data:
                sale_list.append(
                    Sale(SellerInformation(username=row[1], profile_pic=row[2], mail_address=row[3]), sale_id=row[0],
                         sale_start=row[4], sale_end=row[5], item_info=ItemInformation(item_id=row[6],
                                                                                       item_name=row[7],
                                                                                       item_picture=row[8],
                                                                                       item_price=row[9],
                                                                                       item_description=row[10],
                                                                                       item_currency=row[11],
                                                                                       item_city=row[12],
                                                                                       item_country=row[13]
                                                                                       )
                         )
                )

            return sale_list

    @classmethod
    def select_items_by_place(cls, city_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT s.SALE_ID, u.USERNAME, u.PROFILE_PIC, u.MAIL_ADDRESS, s.START_DATE, s.END_DATE, i.*, CITIES.CITY_NAME, CITIES.COUNTRY FROM USERS AS u
                                   INNER JOIN SALES AS s ON s.SELLER_ID=u.USER_ID
                                   INNER JOIN ITEMS AS i ON s.ITEM_ID=i.ITEM_ID
                                   INNER JOIN CURRENCIES AS c ON i.ITEM_CURRENCY=c.CURRENCY_NAME
                                   INNER JOIN CITIES ON s.CITY_ID=CITIES.CITY_ID
                                   WHERE CITIES.CITY_ID=%s
                                   """

            user_data = []

            try:
                cursor.execute(query, (city_id,))
                user_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            sale_list = []

            for row in user_data:
                sale_list.append(
                    Sale(SellerInformation(username=row[1], profile_pic=row[2], mail_address=row[3]), sale_id=row[0],
                         sale_start=row[4], sale_end=row[5], item_info=ItemInformation(item_id=row[6],
                                                                                       item_name=row[7],
                                                                                       item_picture=row[8],
                                                                                       item_price=row[9],
                                                                                       item_description=row[10],
                                                                                       item_currency=row[11],
                                                                                       item_city=row[12],
                                                                                       item_country=row[13]
                                                                                       )
                         )
                )

            return sale_list

    @classmethod
    def select_closest_items(cls, username, city_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT s.SALE_ID, u.USERNAME, u.PROFILE_PIC, u.MAIL_ADDRESS, s.START_DATE, s.END_DATE, i.*, CITIES.CITY_NAME, CITIES.COUNTRY FROM USERS AS u
                                       INNER JOIN SALES AS s ON s.SELLER_ID=u.USER_ID
                                       INNER JOIN ITEMS AS i ON s.ITEM_ID=i.ITEM_ID
                                       INNER JOIN CURRENCIES AS c ON i.ITEM_CURRENCY=c.CURRENCY_NAME
                                       INNER JOIN CITIES ON s.CITY_ID=CITIES.CITY_ID
                                       WHERE u.USERNAME<>%s
                                       ORDER BY
                                       abs((SELECT DISTANCE_TO_CENTER FROM CITIES WHERE CITY_ID=%s)- CITIES.DISTANCE_TO_CENTER)
                                       LIMIT 10
                                       """

            user_data = []

            try:
                cursor.execute(query, (username, city_id))
                user_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            sale_list = []

            for row in user_data:
                sale_list.append(
                    Sale(SellerInformation(username=row[1], profile_pic=row[2], mail_address=row[3]), sale_id=row[0],
                         sale_start=row[4], sale_end=row[5], item_info=ItemInformation(item_id=row[6],
                                                                                       item_name=row[7],
                                                                                       item_picture=row[8],
                                                                                       item_price=row[9],
                                                                                       item_description=row[10],
                                                                                       item_currency=row[11],
                                                                                       item_city=row[12],
                                                                                       item_country=row[13]
                                                                                       )
                         )
                )

            return sale_list

    @classmethod
    def select_items_by_price(cls, username, price, currency):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT s.SALE_ID, u.USERNAME, u.PROFILE_PIC, u.MAIL_ADDRESS, s.START_DATE, s.END_DATE, i.*, CITIES.CITY_NAME, CITIES.COUNTRY FROM USERS AS u
                                           INNER JOIN SALES AS s ON s.SELLER_ID=u.USER_ID
                                           INNER JOIN ITEMS AS i ON s.ITEM_ID=i.ITEM_ID
                                           INNER JOIN CURRENCIES AS c ON i.ITEM_CURRENCY=c.CURRENCY_NAME
                                           INNER JOIN CITIES ON s.CITY_ID=CITIES.CITY_ID
                                           WHERE u.USERNAME<>%s
                                           AND i.ITEM_PRICE * c.CURRENCY_TO_TL < %s * (SELECT CURRENCY_TO_TL FROM CURRENCIES WHERE CURRENCY_NAME=%s)
                                           """

            user_data = []

            try:
                cursor.execute(query, (username, price, currency))
                user_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            sale_list = []

            for row in user_data:
                sale_list.append(
                    Sale(SellerInformation(username=row[1], profile_pic=row[2], mail_address=row[3]), sale_id=row[0],
                         sale_start=row[4], sale_end=row[5], item_info=ItemInformation(item_id=row[6],
                                                                                       item_name=row[7],
                                                                                       item_picture=row[8],
                                                                                       item_price=row[9],
                                                                                       item_description=row[10],
                                                                                       item_currency=row[11],
                                                                                       item_city=row[12],
                                                                                       item_country=row[13]
                                                                                       )
                         )
                )

            return sale_list



sale_ops = SaleDatabaseOPS()
