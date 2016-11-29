from database import database
import psycopg2 as dbapi2

class Group:
    def __init__(self, group_id, group_name, group_pic, group_description):
        self.group_id = group_id
        self.group_name = group_name
        self.group_pic = group_pic
        self.group_description = group_description

class Group_Participation:
    def __init__(self, group_id, user_id):
        self.group_id = group_id
        self.user_id = user_id

class GroupDatabaseOPS:
    @classmethod
    def add_group(cls, group_name, group_pic, group_description):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO GROUPS (GROUP_NAME, GROUP_PIC, GROUP_DESCRIPTION) VALUES (
                                            %s,
                                            %s,
                                            %s
                            ) RETURNING GROUP_ID"""

            try:
                cursor.execute(query, (group_name, group_pic, group_description))
                group_id = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            return group_id

    @classmethod
    def add_group_participation(cls, group_id, user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO GROUP_PARTICIPANTS (GROUP_ID, PARTICIPANT_ID) VALUES (
                                        %s,
                                        %s
                            )"""
            try:
                cursor.execute(query, (group_id, user_id))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def update_group_description(cls, group_id, group_description):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """UPDATE GROUPS SET GROUP_DESCRIPTION = %s WHERE GROUP_ID=%s"""

            try:
                cursor.execute(query, (group_description, group_id,))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def delete_group(cls,group_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM GROUPS WHERE GROUP_ID= %s"""

            try:
                cursor.execute(query, (group_id,))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def find_groups(cls):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM GROUPS"""
            all_groups_data = []

            try:
                cursor.execute(query,)
                all_groups_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()
            groups_list=[]

            for row in all_groups_data:
                groups_list.append(
                    Group(row[0], row[1], row[2], row[3])
                )
            return groups_list


    @classmethod
    def select_group(cls, group_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM GROUPS WHERE GROUP_ID=%s"""

            try:
                cursor.execute(query, (group_id,))
                group = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()


        if group:
            return Group(group[0], group[1], group[2], group[3])
        else:
            return -1

    @classmethod
    def select_group_participation(cls, group_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query= """SELECT * FROM GROUP_PARTICIPANTS WHERE GROUP_ID=%s"""
            participant_data = []
            try:
                cursor.execute(query, (group_id,))
                participant_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

                cursor.close()
            participant_list=[]

            for row in participant_data:
                participant_list.append(
                    Group_Participation(row[0], row[1])
                )
            return participant_list

    @classmethod
    def select_participated_groups(cls, user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query= """SELECT * FROM GROUP_PARTICIPANTS INNER JOIN GROUPS ON GROUP_PARTICIPANTS.GROUP_ID=GROUPS.GROUP_ID WHERE PARTICIPANT_ID=%s"""
            group_data = []
            try:
                cursor.execute(query, (user_id,))
                group_data = cursor.fetchall()

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

                cursor.close()

            group_list=[]

            for row in group_data:
                group_list.append(
                    Group(group_data[2], group_data[3], group_date[4], group_data[5])
                )
            return group_list

group_ops = GroupDatabaseOPS()
