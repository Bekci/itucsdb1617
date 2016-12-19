from database import database
import psycopg2 as dbapi2


class Knot:
    def __init__(self, knot_id, owner_id, knot_content, like_counter, reknot_counter, is_group, post_date):
        self.knot_id = knot_id
        self.owner_id = owner_id
        self.knot_content = knot_content
        self.like_counter = like_counter
        self.reknot_counter = reknot_counter
        self.is_group = is_group
        self.post_date = post_date


class KnotDatabaseOPS:
    @classmethod
    def add_knot(self, owner_id, knot_content, likes, reknots, is_group, post_date):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Tolga Bilbey - KNOTS TABLE ----------------------

            query = """INSERT INTO KNOTS (OWNER_ID, KNOT_CONTENT, LIKE_COUNTER, REKNOT_COUNTER, IS_GROUP, POST_DATE) VALUES (
                                          %s, %s, %s, %s, %s, %s
                        ) RETURNING KNOT_ID"""
            try:
                cursor.execute(query, (owner_id, knot_content, likes, reknots, is_group, post_date))
                knot_id = cursor.fetchone()
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()
            return knot_id

    @classmethod
    def update_knot(self, owner_id, knot_content, likes, reknots, is_group, post_date, knot_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Tolga Bilbey - KNOTS TABLE ----------------------

            query = """UPDATE KNOTS SET OWNER_ID=%s, KNOT_CONTENT=%s, LIKE_COUNTER=%s,
                            REKNOT_COUNTER=%s, IS_GROUP=%s, POST_DATE=%s  WHERE KNOT_ID=%s"""
            try:
                cursor.execute(query, (owner_id, knot_content, likes, reknots, is_group, post_date, knot_id))
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def delete_knot(self, knot_id):
        with dbapi2.connect(database.config) as connection:
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

    @classmethod
    def select_knot(self, knot_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Tolga Bilbey - KNOTS TABLE ----------------------

            query = """SELECT * FROM KNOTS WHERE KNOT_ID=%s"""
            try:
                cursor.execute(query, (knot_id,))
                knot_data = cursor.fetchone()
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            if knot_data:
                return Knot(knot_data[0], knot_data[1], knot_data[2], knot_data[3],
                    knot_data[4], knot_data[5], knot_data[6])
            else:
                return -1


    @classmethod
    def select_knots_for_owner(self, owner_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Tolga Bilbey - KNOTS TABLE ----------------------

            query = """SELECT * FROM KNOTS WHERE OWNER_ID=%s AND IS_GROUP=False ORDER BY POST_DATE DESC"""
            knot_data = []
            knot_list = []
            try:
                cursor.execute(query, (owner_id,))
                knot_data = cursor.fetchall()
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            for row in knot_data:
                knot_list.append(
                    Knot(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                )
            return knot_list

    @classmethod
    def select_knots_for_search(self, content):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Tolga Bilbey - KNOTS TABLE ----------------------
            formatted_string = "%{}%".format(content)
            query = """SELECT * FROM KNOTS WHERE KNOT_CONTENT LIKE %s AND IS_GROUP=False ORDER BY POST_DATE DESC"""
            knot_data = []
            knot_list = []
            try:
                cursor.execute(query, (formatted_string,))
                knot_data = cursor.fetchall()
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            for row in knot_data:
                knot_list.append(
                    Knot(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                )
            return knot_list

    @classmethod
    def get_likes(cls, user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()


            query = """SELECT KNOTS.KNOT_ID, KNOTS.OWNER_ID, KNOTS.KNOT_CONTENT, KNOTS.LIKE_COUNTER,
                              KNOTS.REKNOT_COUNTER, KNOTS.IS_GROUP, KNOTS.POST_DATE
                            FROM LIKE_REKNOT
                            INNER JOIN KNOTS on KNOTS.KNOT_ID = LIKE_REKNOT.KNOT_ID
                            WHERE USER_ID = %s
                            AND LIKE_REKNOT.IS_LIKE = True
                                """
            knot_list = []
            try:
                cursor.execute(query, (user_id,))
                knot_list = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            result = []

            for row in knot_list:
                result.append(
                    Knot(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                )

            return result


knot_ops = KnotDatabaseOPS()
