from database import database
import psycopg2 as dbapi2


class City:
    def __init__(self, city_id, name, distance, country):
        self.id = city_id
        self.name = name
        self.distance_to_center = distance
        self.country = country


class CityDatabaseOPS:
    @classmethod
    def add_city(cls, name, distance, country):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO CITIES (CITY_NAME, DISTANCE_TO_CENTER, COUNTRY) VALUES (
                                              %s,
                                              %s,
                                              %s
                            )"""

            try:
                cursor.execute(query, (name, distance, country))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def delete_city(cls, name, country):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM CITIES WHERE CITY_NAME = %s AND COUNTRY = %s"""

            try:
                cursor.execute(query, (name, country))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def select_city(cls, name, country):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM CITIES WHERE CITY_NAME=%s AND COUNTRY = %s
                       ORDER BY COUNTRY"""

            try:
                cursor.execute(query, (name, country))
                city_data = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            if city_data:
                return City(city_id=city_data[0], name=city_data[1], distance=city_data[2], country=city_data[3])
            else:
                return -1

    @classmethod
    def select_city_by_id(cls, city_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM CITIES WHERE CITY_ID=%s"""

            try:
                cursor.execute(query, (city_id,))
                city_data = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            if city_data:
                return City(city_id=city_data[0], name=city_data[1], distance=city_data[2], country=city_data[3])
            else:
                return -1

    @classmethod
    def select_all_cities(cls):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM CITIES"""

            city_data = []

            try:
                cursor.execute(query, ())
                city_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            user_list = []

            for row in city_data:
                user_list.append(
                    City(city_id=row[0], name=row[1], distance=row[2], country=row[3])
                )

            return user_list


city_ops = CityDatabaseOPS()
