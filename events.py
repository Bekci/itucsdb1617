from database import database
import psycopg2 as dbapi2


class Event:
    def __init__(self, event_id, owner_id, event_content, start_date, end_date, is_user, participants=None):
        self.event_id = event_id
        self.owner_id = owner_id
        self.event_content = event_content
        self.start_date = start_date
        self.end_date = end_date
        self.is_user = is_user
        self.participants = []


class EventDatabaseOPS:
    @classmethod
    def add_event(self, owner_id, event_content, start_date, end_date, is_user):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Tolga Bilbey - EVENTS TABLE ----------------------

            query = """INSERT INTO EVENTS (OWNER_ID, EVENT_CONTENT, EVENT_START_DATE, EVENT_END_DATE, IS_USER) VALUES (
                                          %s, %s, %s, %s, %s
                        ) RETURNING EVENT_ID"""
            try:
                cursor.execute(query, (owner_id, event_content, start_date, end_date, is_user))
                event_id = cursor.fetchone()
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

        return event_id

    @classmethod
    def update_event(self, event_content, start_date, end_date, event_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Tolga Bilbey - EVENTS TABLE ----------------------

            query = """UPDATE EVENTS SET EVENT_CONTENT=%s, EVENT_START_DATE=%s, EVENT_END_DATE=%s  WHERE EVENT_ID=%s"""
            try:
                cursor.execute(query, (event_content, start_date, end_date, event_id))
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def add_participant(self, event_id, user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Tolga Bilbey - EVENTS TABLE ----------------------

            query = """INSERT INTO EVENT_PARTICIPANTS (EVENT_ID, PARTICIPANT_ID) VALUES (
                                          %s, %s
                        )"""
            try:
                cursor.execute(query, (event_id, user_id))
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def delete_participant(self, event_id, user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Tolga Bilbey - EVENTS TABLE ----------------------

            query = """DELETE FROM EVENT_PARTICIPANTS WHERE EVENT_ID=%s AND PARTICIPANT_ID=%s"""
            try:
                cursor.execute(query, (event_id,user_id))
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def delete_event(self, event_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Tolga Bilbey - EVENTS TABLE ----------------------

            query = """DELETE FROM EVENTS WHERE EVENT_ID=%s"""
            try:
                cursor.execute(query, (event_id,))
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def select_event(self, event_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Tolga Bilbey - EVENTS TABLE ----------------------

            query = """SELECT * FROM EVENTS INNER JOIN EVENT_PARTICIPANTS ON EVENTS.EVENT_ID=EVENT_PARTICIPANTS.EVENT_ID WHERE EVENT_ID=%s ORDER BY EVENT_END_DATE DESC"""
            event_list = []
            event_data = []
            participants = []
            try:
                cursor.execute(query, (event_id,))
                event_data = cursor.fetchall()
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            for row in event_data:
                event = Event(row[0], row[1], row[2], row[3], row[4], row[5], None)
                if event.event_id not in [event.event_id for event in event_list]:
                    for row2 in event_data:
                        if row2[0] == event.event_id:
                            participants.append(row2[6])
                    event.participants = participants
                    event_list.append(event)
            return event_list

    @classmethod
    def select_organized_events_with_user_id(self, user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Tolga Bilbey - EVENTS TABLE ----------------------

            query = """SELECT * FROM EVENTS INNER JOIN EVENT_PARTICIPANTS ON EVENTS.EVENT_ID=EVENT_PARTICIPANTS.EVENT_ID WHERE OWNER_ID=%s AND IS_USER=True ORDER BY EVENT_END_DATE DESC"""
            event_data = []
            participants = []
            event_list = []
            try:
                cursor.execute(query, (user_id,))
                event_data = cursor.fetchall()
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()
            event_ids = []
            for row in event_data:
                participants = []
                event = Event(row[0], row[1], row[2], row[3], row[4], row[5], None)
                for row2 in event_data:
                    if row[0] == row2[0]:
                        participants.append(row2[7])
                if not row[0] in event_ids:
                    event_ids.append(row[0])
                    event.participants = participants
                    event_list.append(event)
            return event_list

    @classmethod
    def select_group_events_with_group_id(self, group_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Tolga Bilbey - EVENTS TABLE ----------------------

            query = """SELECT * FROM EVENTS INNER JOIN EVENT_PARTICIPANTS ON EVENTS.EVENT_ID=EVENT_PARTICIPANTS.EVENT_ID WHERE OWNER_ID=%s AND IS_USER=False ORDER BY EVENT_END_DATE DESC"""
            event_data = []
            participants = []
            event_list = []
            try:
                cursor.execute(query, (group_id,))
                event_data = cursor.fetchall()
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()
            event_ids = []
            for row in event_data:
                participants = []
                event = Event(row[0], row[1], row[2], row[3], row[4], row[5], None)
                for row2 in event_data:
                    if row[0] == row2[0]:
                        participants.append(row2[7])
                if not row[0] in event_ids:
                    event_ids.append(row[0])
                    event.participants = participants
                    event_list.append(event)
            return event_list

    @classmethod
    def select_joined_events_with_user_id(self, user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Tolga Bilbey - EVENTS TABLE ----------------------

            query = """SELECT * FROM EVENTS INNER JOIN EVENT_PARTICIPANTS ON EVENTS.EVENT_ID=EVENT_PARTICIPANTS.EVENT_ID WHERE OWNER_ID<>%s AND PARTICIPANT_ID=%s ORDER BY EVENT_END_DATE DESC"""
            event_data = []
            participants = []
            event_list = []
            try:
                cursor.execute(query, (user_id,user_id))
                event_data = cursor.fetchall()
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            event_ids = []
            for row in event_data:
                participants = []
                event = Event(row[0], row[1], row[2], row[3], row[4], row[5], None)
                for row2 in event_data:
                    if row[0] == row2[0]:
                        participants.append(row2[7])
                if not row[0] in event_ids:
                    event_ids.append(row[0])
                    event.participants = participants
                    event_list.append(event)
            return event_list

    @classmethod
    def select_joinable_events_with_user_id(self, user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Tolga Bilbey - EVENTS TABLE ----------------------

            query = """SELECT * FROM EVENTS INNER JOIN EVENT_PARTICIPANTS ON EVENTS.EVENT_ID=EVENT_PARTICIPANTS.EVENT_ID WHERE OWNER_ID<>%s AND PARTICIPANT_ID<>%s AND DATE_PART('day', EVENT_END_DATE::timestamp - CURRENT_DATE::timestamp)>=0 ORDER BY EVENT_END_DATE DESC"""
            event_data = []
            participants = []
            event_list = []
            try:
                cursor.execute(query, (user_id,user_id))
                event_data = cursor.fetchall()
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()
            event_ids = []
            for row in event_data:
                participants = []
                event = Event(row[0], row[1], row[2], row[3], row[4], row[5], None)
                for row2 in event_data:
                    if row[0] == row2[0]:
                        participants.append(row2[7])
                if not row[0] in event_ids:
                    event_ids.append(row[0])
                    event.participants = participants
                    event_list.append(event)
            return event_list

event_ops = EventDatabaseOPS()
