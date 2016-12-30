Parts Implemented by Nurşah Melis Çinar
================================

I implemented the group and messages part with the knots and user relations. In order to use this entities in our website, class of every table has been created.
There are 5 methods which has to be implemented for these classes.

**-Adding Elements**

These methods perform add operation on every table by taking parameters from users.

**-Selecting Elements**

These methods are used for viewing all table elements or selecting a related element according to given parameters.

**-Updating Elements**

These methods changes the value of the elements according to given parameter.

**-Deleting Elements**

These methods removes the elements from tables according to given parameters.

**-Initializing Tables**

Basically it creates the tables if they do not exist already in the system.

Messages Implementation
-------------------------------------------

Messages table has been designed for keeping private interactions between users. In order to use messages database operations, messages class has been defined at the beginning with parameters in object oriented method.

Messages Table
^^^^^^^^^^^^^

Messages table has five main attributes which are:

-MESSAGE_ID as serial primary key
               Primary key for messages table
-MESSAGE_CONTENT as text not null
               Holds the message content sent by current user
-FROM_USER_ID references USERS table USER_ID attribute
               Holds the current user ID
-TO_USER_ID references USERS table USER_ID attribute
               Holds the user whom message will sent
-MESSAGE_DATE as date
               Holds the message sent date

TO_USER_ID and FROM_USER_ID attributes are the foreign keys of this table.

*add_messages* Method
^^^^^^^^^^^^^^^^^^^^^

This method takes content of the message and the users ID’s as parameter in order to insert the message into the database.
Code block for this implementation is below:

.. code-block:: python

  def add_message(cls, content, from_user, to_user):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO MESSAGES (MESSAGE_CONTENT, FROM_USER_ID,
            TO_USER_ID, MESSAGE_DATE) VALUES (
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
 
*update_message* Method
^^^^^^^^^^^^^^^^^^^^^^^^^^

This method works with message ID and message content parameters which content will be taken from the user. It does an update operation on the related message’s content. Message ID will be sent by the selected message from the table.

.. code-block:: python

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

*delete_message* Method
^^^^^^^^^^^^^^^^^^^^^^^^^^

Delete message method takes message id as parameter and deletes the message from table both of the users.

Here is the code block of the related part:

.. code-block:: python

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
 
*select_message* Method
^^^^^^^^^^^^^^^^^^^^^^^^^^

When user wanted to see the message coming from different user, we must take the messages from database one-by-one. This method includes only one message of the current user’s pull operation by sending message ID.

.. code-block:: python

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
                return Message(message_data[0], message_data[1], message_data[2],
                                message_data[3], message_data[4])
            else:
                return -1

*select_messages_for_chat* Method

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

User can see the whole conversation between him/her and selected user by clicking name of the user. So the messages must be pulled from the database by giving user ID’s.
Related method’s code blow:

.. code-block:: python

 def select_messages_for_chat(cls, from_user_id, to_user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
 
            query = """SELECT * FROM MESSAGES WHERE FROM_USER_ID=%s
            AND TO_USER_ID=%s OR FROM_USER_ID=%s AND TO_USER_ID=%s
            ORDER BY MESSAGE_DATE"""
 
            try:
                cursor.execute(query, (from_user_id, to_user_id, to_user_id,
                                        from_user_id, ))
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

*select_messages_for_users* Method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This method includes messages sent to another user selecting operation by sending current user ID.

.. code-block:: python

 def select_messages_for_user(cls, from_user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
 
            query = """SELECT * FROM MESSAGES WHERE FROM_USER_ID=%s
                        ORDER BY MESSAGE_DATE"""
 
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

Groups Implementation
-----------------------------------------

Groups forms important part of the Knitter implementation. It helps users to find new friends from joined groups.

Groups Table
^^^^^^^^^^^^^

Groups table consist of following columns:

-GROUP_ID as serial primary key
               Primary key for messages table
-GROUP_NAME as text and not null
               Holds the name of the group
-GROUP_PIC as varchar(255) and not null
               Cover picture URL
-GROUP_DESCRIPTION as text not null
               Supports the aim of the group.

Groups table do not include a foreign key.

*add_group* Method
^^^^^^^^^^^^^^^^^^^^^^^^^^

This method takes name, content and the cover picture from the user and adds the given values to the groups table. After the adding operation, it return the group ID.

.. code-block:: python

 def add_group(cls, group_name, group_pic, group_description):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO GROUPS (GROUP_NAME, GROUP_PIC, GROUP_DESCRIPTION)
            VALUES (
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

*update_group* Method
^^^^^^^^^^^^^^^^^^^^^^^^^^

Update operation takes the group ID and the new description entered by the users and updates the values in the given group.

Code part of this method is below:

.. code-block:: python

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
 
*find_groups* Method
^^^^^^^^^^^^^^^^^^^^^^^^^^

This method does not take any parameter. It finds all the groups for listing the groups on the home page so it return an array of groups.

.. code-block:: python

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
 
*select_group* Method
^^^^^^^^^^^^^^^^^^^^^^^^^^

This method brings the group’s rows according to given group ID. It is used for group page view operation.

.. code-block:: python

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

*delete_group* Method
^^^^^^^^^^^^^^^^^^^^^^^^^^

This method takes the group ID as parameter and deletes the group from the table.

Method’s code is below:

.. code-block:: python

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
Group Participation  Implementation
--------------------------------------------------------------

The relation between groups and group participants must be hold in a relational table which called group participants.

Group Participants Table
^^^^^^^^^^^^^^^^^^^^^

This table consist of two columns:

GROUP_ID references groups table serial primary key
		Foreign key
USER_ID References users table serial primary key
		Foreign Key

*add_group_participation* Method 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This method adds the users to the currently selected group by sending user ID and group id.

.. code-block:: python

 def add_group_participation(cls, group_id, user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO GROUP_PARTICIPANTS (GROUP_ID, PARTICIPANT_ID)
            VALUES (
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

*select_group_participation* Method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This method finds the users which has been already joined to group in order to list them.

.. code-block:: python

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

*select_participated_group_list* Method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This method takes parameter user Id and returns the user's participated groups.

.. code-block:: python

 def select_participated_groups(cls, user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query= """SELECT * FROM GROUP_PARTICIPANTS INNER JOIN GROUPS
            ON GROUP_PARTICIPANTS.GROUP_ID=GROUPS.GROUP_ID WHERE PARTICIPANT_ID=%s"""
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
                    Group(row[2], row[3], row[4], row[5])
                )
            return group_list

*exit_group_participation* Method

Users can quit from a group by clicking the join button of the group page. This method takes current user's ID as parameter and deletes the relation of group and user.

.. code-block:: python

 def exit_group_participation(cls, group_id, user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM GROUP_PARTICIPANTS WHERE PARTICIPANT_ID=%s
            AND GROUP_ID=%s """

            try:
                cursor.execute(query, (group_id, user_id))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()

Group Knot Implementation
----------------------------------------------

Users can add knots to groups so knot and group relation must be holded on a table. Group Knot table holds the values where is_group attribute is true on a selected knot.

Group Knots Table
^^^^^^^^^^^^^^^

This table has two columns in order to hold knots for groups.

KNOT_ID references knot table serial primary key
		Holds the knot ID's

GROUP_ID references groups table serial primary key

		Holds the group ID's.

*add_group_knot* Method

This method adds a relation between groups and knots into the table in order to show the knotw on the selected group page.

Code block of this part is below:

.. code-block:: python

 def add_group_knot(cls, group_id, knot_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO GROUP_KNOT (GROUP_ID, KNOT_ID) VALUES (
                                        %s,
                                        %s
                            )"""
            try:
                cursor.execute(query, (group_id, knot_id))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

*select_group_knot* Method

Knots can be selected by sending the group id as a parameter an returns the knot rows.

.. code-block:: python

 def select_group_knot(cls, group_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query= """SELECT * FROM GROUP_KNOT WHERE GROUP_ID=%s"""
            knot_data = []
            try:
                cursor.execute(query, (group_id,))
                knot_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

                cursor.close()

            knot_list=[]
            for row in knot_data:
                knot_list.append(
                    Group_Knot(row[0], row[1])
                )
            return knot_list
