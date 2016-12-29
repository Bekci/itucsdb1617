Parts Implemented by Ozan ATA
================================

Getting the Notifications:
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
