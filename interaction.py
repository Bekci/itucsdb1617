from database import database
import psycopg2 as dbapi2


class Interaction:
    def __init__(self, base_id, target_id):
        self.base_user_id = base_id
        self.target_user_id = target_id


class InteractionDatabaseOPS:
    @classmethod
    def add_user_interaction(cls, base_id, target_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - USER_INTERACTION TABLE -----------------------

            query = """INSERT INTO USER_INTERACTION(BASE_USER_ID, TARGET_USER_ID) VALUES(
                                                    %s,
                                                    %s
                        )"""

            try:
                cursor.execute(query, (base_id, target_id))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def delete_user_interaction(cls, base_id, target_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - USER_INTERACTION TABLE -----------------------

            query = """DELETE FROM USER_INTERACTION WHERE BASE_USER_ID = %s AND TARGET_USER_ID = %s"""

            try:
                cursor.execute(query, (base_id, target_id))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def select_followings_from_user_interaction(cls, base_id):  # base id keeps followers
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - USER_INTERACTION TABLE -----------------------

            query = """SELECT TARGET_USER_ID FROM USER_INTERACTION WHERE BASE_USER_ID = %s"""
            followings_ids = []
            followings_list = []
            try:
                cursor.execute(query, (base_id,))
                followings_ids = cursor.fetchall()
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            for person in followings_ids:
                followings_list.append(
                    Interaction(
                        base_id,  # base user
                        person[1]  # following user by base user
                    )
                )
            return followings_list

    @classmethod
    def select_followers_from_user_interaction(cls, target_id):  # target_id keeps followings
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - USER_INTERACTION TABLE -----------------------

            query = """SELECT BASE_USER_ID FROM USER_INTERACTION WHERE TARGET_USER_ID = %s"""
            followers_ids = []
            followers_list = []

            try:
                cursor.execute(query, (target_id,))
                followers_ids = cursor.fetchall()
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            for person in followers_ids:
                followers_list.append(
                    Interaction(
                        target_id,  # target user
                        person[1]  # follower user of target user
                    )
                )
            return followers_list

    @classmethod
    def select_interactions_for_search(cls, base_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - USER_INTERACTION TABLE -----------------------

            query = """SELECT * FROM USER_INTERACTION WHERE BASE_USER_ID = %s"""
            interactions_ids = []
            interactions_list = []

            try:
                cursor.execute(query, (base_id,))
                interactions_ids = cursor.fetchall()
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            for person in interactions_ids:
                interactions_list.append(
                    Interaction(
                        base_id,
                        person[1]
                    )
                )
            return interactions_list
# An update operation can not be performed on user_interaction table.
# When a base user unfollows another target user, that means, there is no interaction between each other and it requires a delete operation.
# Also, when a base user follows another target user, that requires an insert operation because of the follow interaction between users.
# As a result of that, any record in user_interaction table is not updated for follow/unfollow operations.

interaction_ops = InteractionDatabaseOPS()
