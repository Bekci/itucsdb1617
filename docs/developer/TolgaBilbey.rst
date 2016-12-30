Parts Implemented by Tolga Bilbey
================================

Knots, Events, Event_Participants tables are created by me. 

Knots Table & Functions
----------------------------------------

The columns of Knots table are given below.

* KNOT_ID SERIAL PRIMARY KEY
    This is serial primary key for knots
*  OWNER_ID INTEGER NOT NULL REFERENCES USERS(USER_ID) ON DELETE CASCADE ON UPDATE CASCADE
    Owner information kept by using foreign key
*  KNOT_CONTENT TEXT
     Content of knot is kept here
*  LIKE_COUNTER INTEGER DEFAULT 0
     Like counter of knot is kept here
*   REKNOT_COUNTER INTEGER DEFAULT 0
     Reknot counter of knot is kept here
*   IS_GROUP BOOLEAN NOT NULL
      Knot is added by user and groups. This field shows who added the knot.
*   POST_DATE DATE NOT NULL
      The date which knot is created

In knot.py file KnotDatabaseOPS class is created and all knot related functions are in this class.

*Adding Knot*
^^^^^^^^^^^^^

.. code-block:: python

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

*Updating Knot*
^^^^^^^^^^^^^^^

.. code-block:: python
	
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

*Deleting Knot*
^^^^^^^^^^^^^^^^

.. code-block:: python

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

*Selecting Knot*
^^^^^^^^^^^^^^^^

There are three different type of select function. First function gets a parameter of knot id to select a knot.
 
.. code-block:: python

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

Secondly, knot can be selected by using owner id.

.. code-block:: python

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

Thirdly, search page is using select_knots_for_search function. It filters whole knot table with IS_GROUP=False which is required for selecting knot which is created by user not group. Also it uses like to get knot with given content.

.. code-block:: python

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

Events Table & Functions
-------------------------------------------

The columns of Events table are given below.

* EVENT_ID SERIAL PRIMARY KEY
    This is the serial primary key for event.
* OWNER_ID INTEGER NOT NULL
    This is used by both groups and users. It stores an id.
* EVENT_CONTENT TEXT
    Content is kept here.
* EVENT_START_DATE DATE NOT NULL
    Start date is stored here.
* EVENT_END_DATE DATE NOT NULL
    End date is kept here.
* IS_USER BOOLEAN NOT NULL
    It is used for understanding this event is created by whom a user or a group

In events.py file EventDatabaseOPS class is created.

*Adding Event*
^^^^^^^^^^^^^^

.. code-block:: python 

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

*Updating Event*
^^^^^^^^^^^^^^^^

.. code-block:: python    
 
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

*Deleting Event*
^^^^^^^^^^^^^^^

.. code-block:: python

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

*Selecting Event*
^^^^^^^^^^^^^^^^^

There are 5 select functions for event table. First of all event can be selected by event id.

.. code-block:: python

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

Secondly, events can be selected by using user id. Below function is selecting events according to user id and it selects the knots which are created by users not groups. 

.. code-block:: python

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

Thirdly, events can be selected by group id. Below function is selecting events which are created by groups.

.. code-block:: python

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

Fourthly, events can be selected with using user id. It is different from the one above because it selects the events whose participant is the user and this user is not the organizer of this event.

.. code-block:: python

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

At last, events can be selected by using id. It is different from the ones above. It selects the events whose organizer is not the user and whose participant is not the user.

.. code-block:: python

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

Event Participant Table & Functions
------------------------------------------------------------

Event Participant table is created for Events table. It stores the participant of events.

The columns of Event Participant table is given below.

* EVENT_ID INTEGER NOT NULL REFERENCES EVENTS(EVENT_ID) ON DELETE CASCADE ON UPDATE CASCADE
    This column kepts the event information.
* PARTICIPANT_ID INTEGER NOT NULL REFERENCES USERS(USER_ID) ON DELETE CASCADE ON UPDATE CASCADE
    This column stores the user information that is a participant of an event.

*Adding Participant*
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

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

*Deleting Participant*
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

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

Other Implementations
----------------------------------------

I wrote a javascript function to get the information of is_user in events page. 

.. code-block:: javascript

  <script>
    function get_is_user(){

      $("#is_user").val($("#Organizer").prop('selectedIndex'));
    };
   </script>

I also wrote a javascript function get the information of to_user in messages page.

.. code-block:: javascript

   <script>
		function get_to_id(id){
			$("#to_user_response_id").val(id);
		};
    </script>

Another implementation that I do is using context_processors in templates which is useful to call function in templates.

.. code-block:: python

  def utility_processor():

    def get_real_name(user_id):
        user = UserDatabaseOPS.select_user_with_id(user_id)
        real_name = UserDatabaseOPS.select_user_detail(user.username)
        return real_name

    def get_user_info(user_id):
        user = UserDatabaseOPS.select_user_with_id(user_id)
        return user

    def get_group_info(group_id):
        group = GroupDatabaseOPS.select_group(group_id)
        return group

    return dict(get_real_name=get_real_name, get_user_info=get_user_info, get_group_info=get_group_info)

Flask-Login implementation which is in the documents and errorhandler for 403 and 404 is done by me.

*Using Error Handlers*
^^^^^^^^^^^^^^^^^^^

If in the handlers.py there is an error and abort function is called, error handlers catches this error code and renders the required html files.

To use error handlers I added these to server.py.

.. code-block:: python

 @app.errorhandler(403)
 def page_forbidden(e):
    return render_template('403.html'), 403

 @app.errorhandler(404)
 def page_not_found(e):
    return render_template('404.html'), 404

*Flask-Login Plugin Implementation*
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 
To use flask-login plugin I added these to server.py.

.. code-block:: python

  lm = LoginManager()
  
  def create_app():
     ...
     lm.init_app(app)
     lm.login_view = 'site.login_page'
     app.secret_key = '<secret>'
     ...
     return app

  @lm.user_loader
  def load_user(user_id):
    return UserDatabaseOPS.select_user_with_id(user_id)

I also added UserMixin to User class in user.py.

After these configurations and adding Flask-Login to requirements.txt. Flask-Login plugin is activated. Flask-Login has login_user, logout_user methods to keeping track of user login status. Also login_required decorator is useful for permission checking. current_user variable is available in both python files and templates.
  