Parts Implemented by Ozan Ata
================================

Getting the Notifications
-----------------------------
To get the notifications, we need to keep track of the knot(target), user(action_source) and action_type(is it a like or not)
we keep those in a table called like_reknot.

.. code-block:: python

  query = """CREATE TABLE IF NOT EXISTS LIKE_REKNOT(
                    KNOT_ID INTEGER references KNOTS(KNOT_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                    USER_ID INTEGER references USERS(USER_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                    IS_LIKE BOOLEAN
             )"""
  cursor.execute(query)
  
  
And to get notifications we use the following query to get all the notifications for the active_user.

.. code-block:: python

  query = """SELECT
                knots.knot_id as knot_id,
                knots.knot_content as knot_content,
                knots.like_counter as like_number,
                knots.reknot_counter as reknot_number,
                users.profile_pic as action_source_pic,
                users.username as action_source,		  
                like_reknot.is_like as action_is_like                   
            from like_reknot                
                inner join users on like_reknot.user_id = users.user_id
                INNER JOIN knots on knots.knot_id = like_reknot.knot_id
                where knots.owner_id = %s;        
            """
            
        cursor.execute(query,[active_user.id])

        
How this query works? It selects knots with active_user.id as knot.owner.id, with two inner join, returns the target_knot's information and action_source user's information.

Like and Re-Knot
-----------------------------

How like and re-knot works? When the active user clicks the like button it runs the following script

.. code-block:: python

    query = """UPDATE KNOTS SET LIKE_COUNTER= LIKE_COUNTER+1 WHERE KNOT_ID=%s"""

    cursor.execute(query, (knot_id))
    
    # then
    
    query = """INSERT INTO LIKE_REKNOT (KNOT_ID, USER_ID, IS_LIKE) VALUES (
                        %s,
                        %s,
                        %s
                    )"""

    cursor.execute(query, (knot_id, user_id, is_like))

When the active user clicks the like button, on a knot which he/she already liked. It runs the following script

.. code-block:: python

    query = """UPDATE KNOTS SET LIKE_COUNTER=LIKE_COUNTER-1 WHERE KNOT_ID=%s"""

    cursor.execute(query, (knot_id))
    # then
    
    query = """ DELETE FROM LIKE_REKNOT
                    WHERE
                    knot_id=%s and
                    user_id=%s and
                    is_like=%s"""
                    
    cursor.execute(query, (knot_id,user_id, is_like))

Using Polls
-----------------------------

Polls are stored in a table called Polls, which is created with the following script

.. code-block:: python

    query = """CREATE TABLE IF NOT EXISTS POLLS(
                    POLL_ID SERIAL PRIMARY KEY,
                    OWNER_ID INTEGER references USERS(USER_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                    POLL_CONTENT varchar(255) NOT NULL,
                    POLL_OPTION_1_CONTENT varchar(255) NOT NULL,
                    POLL_OPTION_1_COUNTER INTEGER DEFAULT 0,
                    POLL_OPTION_2_CONTENT varchar(255) NOT NULL,
                    POLL_OPTION_2_COUNTER INTEGER DEFAULT 0,
                    START_DATE date NOT NULL,
                    END_DATE date NOT NULL
                    )"""

    cursor.execute(query)

When a user votes a poll, it is stored in a relation table named user_poll. By doing this, we prevent users from voting a single poll multiple times. This process is handled using the following scripts

.. code-block:: python

    query = """UPDATE POLLS SET POLL_OPTION_1_COUNTER= POLL_OPTION_1_COUNTER+1 WHERE POLL_ID=%s"""

    cursor.execute(query, (poll_id))
    
    # then
    
    query = """INSERT INTO USER_POLL (POLL_ID, USER_ID) VALUES(%s, %s)"""

    cursor.execute(query, (poll_id,user_id))
    
Following and Unfollowing Users
-----------------------------

Following and unfollowing processes are handled on the user_interaction table. It only has two columns called base_user_id and target_user_id ,in other words action_source and action_target. Follow and unfollow operations insert  a new relation to this table or removes a row from this table.

.. code-block:: python

    query = """INSERT INTO user_interaction (base_user_id, target_user_id)
                          VALUES (%s, %s)
            """

    cursor.execute(query, (user_id, target_user))

    query = """delete from user_interaction
                    where 
                base_user_id = %s
                and target_user_id = %s
            """

    cursor.execute(query, (user_id, target_user))
    
    
Get Followings
-----------------------------
In user_profile page, user can see the users that he/she already follow. Followings are selected with the following query

.. code-block:: python

    query = """SELECT USERS.PROFILE_PIC, USERS.USERNAME, USERS.USER_ID  FROM USER_INTERACTION
           INNER JOIN USERS ON USERS.USER_ID=USER_INTERACTION.TARGET_USER_ID
           WHERE USER_INTERACTION.BASE_USER_ID = %s
                    """
                    
    cursor.execute(query, (user_id,))


Get Followers
-----------------------------
In user_profile page, user can see the users that already follow him/her. Followers are selected with the following query

.. code-block:: python

    query = """SELECT USERS.PROFILE_PIC, USERS.USERNAME, USERS.USER_ID FROM USER_INTERACTION
               INNER JOIN USERS ON USERS.USER_ID=USER_INTERACTION.BASE_USER_ID
               WHERE USER_INTERACTION.TARGET_USER_ID = %s
            """

    cursor.execute(query, (user_id,))
                
                
                
Get Likes
-----------------------------
In user_profile page, user can see the knots that he/she liked before. Liked knots selected with the following query

.. code-block:: python

    query = """SELECT KNOTS.KNOT_ID, KNOTS.OWNER_ID, KNOTS.KNOT_CONTENT, KNOTS.LIKE_COUNTER,
                  KNOTS.REKNOT_COUNTER, KNOTS.IS_GROUP, KNOTS.POST_DATE,
                FROM LIKE_REKNOT
                INNER JOIN KNOTS on KNOTS.KNOT_ID = LIKE_REKNOT.KNOT_ID
                WHERE LIKE_REKNOT.USER_ID = %s
                AND LIKE_REKNOT.IS_LIKE = True
                    """
    cursor.execute(query, (user_id,))
    
Handlers.py
-----------------------------
handlers.py for notifications_page

.. code-block:: python

    @site.route('/notifications/<int:user_id>', methods = ['GET','POST'])
    @login_required
    def notifications_page(user_id):
        user = UserDatabaseOPS.select_user_with_id(user_id)
        if current_user != user:
            abort(403)
        trends = Trend(30,70)
        knots = NotificationDatabaseOPS.select_notifications(user)
        polls = []
        polls = PollDatabaseOPS.select_poll(user.id)

        if request.method == 'GET':
            return render_template('notifications.html', signedin=True,trends=trends,knots=knots, user = user, polls = polls)

        else:
            if 'delete_knot' in request.form:
                knot_id = request.form['delete_knot']
                KnotDatabaseOPS.delete_knot(knot_id)

            elif 'update' in request.form:
                knot_id = request.form['update']
                print("Update Knot function is currently not working :(")

            elif 'like' in request.form:
                knot_id = request.form['like']
                is_like = NotificationDatabaseOPS.check_like(knot_id,user.id, True)
                if is_like:
                    NotificationDatabaseOPS.delete_relation(knot_id, user.id, True)
                    NotificationDatabaseOPS.decrease_knot_like(knot_id)
                else:
                    NotificationDatabaseOPS.insert_relation(knot_id, user.id, True)
                    NotificationDatabaseOPS.increase_knot_like(knot_id)

            elif 'reknot' in request.form:
                knot_id = request.form['reknot']
                is_reknot = NotificationDatabaseOPS.check_reknot(knot_id,user.id, False)
                if is_reknot:
                    NotificationDatabaseOPS.delete_relation(knot_id, user.id, False)
                    NotificationDatabaseOPS.decrease_knot_reknot(knot_id)
                else:
                    NotificationDatabaseOPS.insert_relation(knot_id, user.id, False)
                    NotificationDatabaseOPS.increase_knot_reknot(knot_id)

            elif 'create' in request.form:
                PollDatabaseOPS.add_poll(user.id, request.form['poll_content'], request.form['answer_1'], request.form['answer_2'], datetime.now().date().isoformat(), request.form['end_date'])

            elif 'vote' in request.form:
                PollDatabaseOPS.update_poll(int(request.form['optionsRadios']),request.form['id'])
                PollDatabaseOPS.add_relation(user.id,request.form['id'])

            elif 'delete_poll' in request.form:
                if user.id == int(request.form['owner']):
                    PollDatabaseOPS.delete_poll(request.form['id'])
            else:
                print(request.form)

            polls = PollDatabaseOPS.select_poll(user.id)
            knots = NotificationDatabaseOPS.select_notifications(user)
            return render_template('notifications.html', signedin=True,trends=trends,knots=knots, user = user, polls = polls)


handlers.py for search_page

.. code-block:: python

    @site.route('/search/<int:user_id>/<query>', methods=['GET', 'POST'])
    @login_required
    def search_page(user_id, query):
        user = UserDatabaseOPS.select_user_with_id(user_id)
        if current_user != user:
            abort(403)
        if request.method == 'GET':
            query_in_users = UserDatabaseOPS.select_users_for_search(query,user_id)
            query_in_knots = KnotDatabaseOPS.select_knots_for_search(query)
            return render_template('search_page.html',signed_in=True,user=user,users=query_in_users, knots=query_in_knots, query=query)
        else:
            if 'delete_knot' in request.form:
                knot_id = request.form['delete_knot']
                print("Update Knot function is not working on the Search Page :(")

            elif 'update' in request.form:
                knot_id = request.form['update']
                print("Update Knot function is not working on the Search Page :(")

            elif 'like' in request.form:
                knot_id = request.form['like']
                is_like = NotificationDatabaseOPS.check_like(knot_id,user.id, True)
                if is_like:
                    NotificationDatabaseOPS.delete_relation(knot_id, user.id, True)
                    NotificationDatabaseOPS.decrease_knot_like(knot_id)
                else:
                    NotificationDatabaseOPS.insert_relation(knot_id, user.id, True)
                    NotificationDatabaseOPS.increase_knot_like(knot_id)

            elif 'reknot' in request.form:
                knot_id = request.form['reknot']
                is_reknot = NotificationDatabaseOPS.check_reknot(knot_id,user.id, False)
                if is_reknot:
                    NotificationDatabaseOPS.delete_relation(knot_id, user.id, False)
                    NotificationDatabaseOPS.decrease_knot_reknot(knot_id)
                else:
                    NotificationDatabaseOPS.insert_relation(knot_id, user.id, False)
                    NotificationDatabaseOPS.increase_knot_reknot(knot_id)

            elif 'follow' in request.form:
                target_user = request.form['target_user']
                UserDatabaseOPS.follow(user_id,target_user)

            elif 'unfollow' in request.form:
                target_user = request.form['target_user']
                UserDatabaseOPS.unfollow(user_id,target_user)

            else:
                print(request.form)

            query_in_users = UserDatabaseOPS.select_users_for_search(query,user_id)
            query_in_knots = KnotDatabaseOPS.select_knots_for_search(query)
            return render_template('search_page.html',signed_in=True,user=user,users=query_in_users, knots=query_in_knots, query=query)
