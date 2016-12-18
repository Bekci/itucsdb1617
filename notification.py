from database import database
import psycopg2 as dbapi2


class Notification:
    def __init__(self,knot_id, knot_content, user_pic_url, username, like_number, reknot_number , action_source_pic, action_source, action_type):
        self.knot_id = knot_id
        self.knot_content = knot_content
        self.user_pic_url = user_pic_url
        self.username = username
        self.like_number = like_number
        self.reknot_number = reknot_number
        self.action_source_pic = action_source_pic
        self.action_source = action_source
        self.action_type = action_type


class NotificationDatabaseOPS:
    @classmethod
    def select_notifications(self, user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            # ----------- Ozan ATA - Get Notifications -----------

            first_query = []
            query = """SELECT
                            knots.knot_id as knot_id,
                            knots.knot_content as knot_content,
                            users.profile_pic AS user_pic_url,
                            users.username AS username,
                            knots.like_counter AS like_number,
                            knots.reknot_counter AS reknot_number
                        FROM knots
                            INNER JOIN users ON knots.owner_id = users.user_id
                            INNER JOIN like_reknot ON knots.knot_id = like_reknot.knot_id
                            where like_counter > 0 OR reknot_counter > 0;"""


            try:
                cursor.execute(query)
                first_query = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()

            second_query = []
            query = """SELECT
                            users.profile_pic as action_source_pic,
                            users.username as action_source,
                            like_reknot.is_like as action_is_like
                        from like_reknot
                            inner join users on like_reknot.user_id = users.user_id
                            INNER JOIN knots on knots.knot_id = like_reknot.knot_id
                            where knots.owner_id = %s;"""
            try:
                cursor.execute(query,[user_id.id])
                second_query = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()
            if len(first_query) > 0 and len(second_query) > 0:
                i = 0
                max = len(second_query)
                result = []

                while i < max:
                    if second_query[i][2] == True:
                        action_type = 'liked'
                    else:
                        action_type = 'reknotted'

                    result.append(Notification(first_query[i][0], first_query[i][1], first_query[i][2] , first_query[i][3], first_query[i][4], first_query[i][5], second_query[i][0], second_query[i][1], action_type))
                    i = i + 1

                return result

            else:
                return []

    @classmethod
    def check_like(self, knot_id, user_id, is_like):
            with dbapi2.connect(database.config) as connection:
                cursor = connection.cursor()

                # ----------- Ozan Ata - Check Like Existance -----------

                query = """SELECT * FROM LIKE_REKNOT
                            WHERE
                            knot_id=%s and
                            user_id=%s and
                            is_like=%s
                            """

                try:
                    cursor.execute(query, (knot_id,user_id,is_like))
                    like_existance = cursor.fetchone()
                except dbapi2.Error:
                    connection.rollback()
                else:
                    connection.commit()

                cursor.close()

                if like_existance is not None:
                    return True
                else:
                    return False

    @classmethod
    def check_reknot(self, knot_id, user_id, is_like):
            with dbapi2.connect(database.config) as connection:
                cursor = connection.cursor()

                # ----------- Ozan ATA - Check Reknot Existance -----------

                query = """SELECT * FROM LIKE_REKNOT
                            WHERE
                            knot_id=%s and
                            user_id=%s and
                            is_like=%s
                            """

                try:
                    cursor.execute(query, (knot_id,user_id,is_like))
                    reknot_existance = cursor.fetchone()
                except dbapi2.Error:
                    connection.rollback()
                else:
                    connection.commit()

                cursor.close()

                if reknot_existance:
                    return True
                else:
                    return False

    @classmethod
    def insert_relation(self,knot_id, user_id, is_like):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            # ----------- Ozan ATA - INSERT RELATION -----------
            query = """INSERT INTO LIKE_REKNOT (KNOT_ID, USER_ID, IS_LIKE) VALUES (
                        %s,
                        %s,
                        %s
                    )"""

            try:
                cursor.execute(query, (knot_id, user_id, is_like))
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def delete_relation(self,knot_id, user_id, is_like):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            # ----------- Ozan ATA - DELETE RELATION -----------
            query = """ DELETE FROM LIKE_REKNOT
                    WHERE
                    knot_id=%s and
                    user_id=%s and
                    is_like=%s"""
            try:
                cursor.execute(query, (knot_id,user_id, is_like))
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def increase_knot_like(self, knot_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Ozan ATA - UPDATE LIKE -----------

            query = """UPDATE KNOTS SET LIKE_COUNTER= LIKE_COUNTER+1 WHERE KNOT_ID=%s"""
            try:
                cursor.execute(query, (knot_id))
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def decrease_knot_like(self, knot_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Ozan ATA - UPDATE LIKE -----------

            query = """UPDATE KNOTS SET LIKE_COUNTER=LIKE_COUNTER-1 WHERE KNOT_ID=%s"""
            try:
                cursor.execute(query, (knot_id))
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def increase_knot_reknot(self, knot_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Ozan ATA - UPDATE REKNOT -----------

            query = """UPDATE KNOTS SET REKNOT_COUNTER=REKNOT_COUNTER+1 WHERE KNOT_ID=%s"""
            try:
                cursor.execute(query, (knot_id))
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def decrease_knot_reknot(self, knot_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Ozan ATA - UPDATE REKNOT -----------

            query = """UPDATE KNOTS SET REKNOT_COUNTER=REKNOT_COUNTER-1 WHERE KNOT_ID=%s"""
            try:
                cursor.execute(query, (knot_id))
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()


notification_ops = NotificationDatabaseOPS()
