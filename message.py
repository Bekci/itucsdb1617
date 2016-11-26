from database import database
import psycopg2 as dbapi2


class Message:
    def __init__(self, message_id, message_content, from_user_id, to_user_id, message_date):
        self.message_id = message_id
        self.message_content = message_content
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.message_date = message_date


class MessageDatabaseOPS:
    @classmethod
    def add_message(cls, content, from_user, to_user):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO MESSAGES (MESSAGE_CONTENT, FROM_USER_ID, TO_USER_ID, MESSAGE_DATE) VALUES (
                                              %s,
                                              %s,
                                              %s,
                                              CURRENT_DATE
                            )"""

            try:
                cursor.execute(query, (content, from_user, to_user))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def update_message(cls, message_id, message_content):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """UPDATE MESSAGES SET MESSAGE_CONTENT=%s WHERE MESSAGE_ID=%s"""

            try:
                cursor.execute(query, (message_content, message_id,))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def delete_message(cls, id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM MESSAGES WHERE MESSAGE_ID = %s"""

            try:
                cursor.execute(query, (id,))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def select_message(cls, id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM MESSAGES WHERE MESSAGE_ID=%s"""

            try:
                cursor.execute(query, (id,))
                message_data = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

                cursor.close()

            if message_data:
                return Message(message_data[0], message_data[1], message_data[2], message_data[3], message_data[4])
            else:
                return -1

    @classmethod
    def select_messages_for_chat(cls, from_user_id, to_user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM MESSAGES WHERE FROM_USER_ID=%s AND TO_USER_ID=%s OR FROM_USER_ID=%s AND TO_USER_ID=%s ORDER BY MESSAGE_DATE"""

            try:
                cursor.execute(query, (from_user_id, to_user_id, to_user_id, from_user_id, ))
                message_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

                cursor.close()

            message_list = []
            for row in message_data:
                message_list.append(
                    Message(row[0], row[1], row[2], row[3], row[4])
                )
            return message_list

    @classmethod
    def select_messages_for_user(cls, from_user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM MESSAGES WHERE FROM_USER_ID=%s ORDER BY MESSAGE_DATE"""

            try:
                cursor.execute(query, (from_user_id, ))
                message_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

                cursor.close()

            message_list = []
            for row in message_data:
                message_list.append(
                    Message(row[0], row[1], row[2], row[3], row[4])
                )
            return message_list


message_ops = MessageDatabaseOPS
