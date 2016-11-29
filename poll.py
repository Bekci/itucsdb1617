from database import database
import psycopg2 as dbapi2
from datetime import datetime
import math

# ------------o Ozan ATA / 150130039 o------------

class Poll:
    def __init__(self, id, owner_id, content, option_1, option_1_counter, option_2, option_2_counter, start_date, end_date, is_voted):
        self.id = id
        self.owner_id = owner_id
        self.content = content
        self.option_1 = option_1
        self.option_1_counter = option_1_counter
        self.option_2 = option_2
        self.option_2_counter = option_2_counter
        self.start_date = start_date
        self.end_date = end_date
        self.is_voted = is_voted


class PollDatabaseOPS:
    @classmethod
    def add_poll(self,owner_id, content, option_1, option_2, start_date, end_date):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO POLLS (OWNER_ID, POLL_CONTENT, POLL_OPTION_1_CONTENT, POLL_OPTION_2_CONTENT, START_DATE, END_DATE) VALUES (
                                              %s,
                                              %s,
                                              %s,
                                              %s,
                                              %s,
                                              %s
                            )"""

            try:
                cursor.execute(query, (owner_id, content, option_1, option_2,start_date, end_date))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()
    
    @classmethod
    def update_poll(self, option_number, poll_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            if option_number == 1:
                query = """UPDATE POLLS SET POLL_OPTION_1_COUNTER= POLL_OPTION_1_COUNTER+1 WHERE POLL_ID=%s"""

            else:
                query = """UPDATE POLLS SET POLL_OPTION_2_COUNTER= POLL_OPTION_2_COUNTER+1 WHERE POLL_ID=%s"""

            try:
                cursor.execute(query, (poll_id))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()
    
    @classmethod
    def add_relation(self,user_id,poll_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO USER_POLL (POLL_ID, USER_ID) VALUES(%s, %s)"""

            try:
                cursor.execute(query, (poll_id,user_id))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def delete_poll(self, poll_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM POLLS WHERE POLL_ID = %s"""

            try:
                cursor.execute(query, (poll_id))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def select_poll(self, user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            user_data = []
            user_votes = []
            current_date = datetime.now().date().isoformat()

            query = """SELECT * FROM POLLS 
                        WHERE END_DATE > CURRENT_DATE 
                        limit 10       
                    """

            try:
                cursor.execute(query)
                user_data = cursor.fetchall()
                
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            query = """SELECT poll_id FROM user_poll 
                        WHERE user_id = %s
                    """

            try:
                cursor.execute(query, [user_id])
                user_votes = cursor.fetchall()
                print(user_votes)
                
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            result = []
            for data in user_data:
                if data[4] == 0 or data[6] == 0:
                    if data[4] > 0:
                        option_1_percent = 100
                        option_2_percent = 0
                    else:
                        option_1_percent = 0
                        option_2_percent = 100
                else: 
                    option_1_percent = math.floor(100*data[4]/(data[4]+data[6]))
                    option_2_percent = 100- option_1_percent
                is_voted = False
                for vote in user_votes:
                    if data[0] == vote[0]:
                        is_voted = True
                result.append(Poll(data[0],data[1],data[2],data[3],option_1_percent,data[5],option_2_percent,data[7],data[8],is_voted))
            return result   

poll_ops = PollDatabaseOPS()
