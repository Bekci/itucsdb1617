Parts Implemented by Can Yılmaz Altıniğne
=========================================

Users, User Detail, Currencies, Items, Sales and Cities tables are created by myself. Select, Update, Delete and Insert
operations for these tables are written and used in all around the web application. Also in handlers.py file necessary
connections between these database operations and the HTML files that I created are made. The operations that I defined
are used by other team mates in their pages.

Users Table & Functions
-----------------------
Users Table is the heart of the Knitter. Almost every table has a reference to this table and the functions of this
table are used widely.

The columns of Users table are given below.

* USER_ID SERIAL PRIMARY KEY
   This is serial primary key for users
* USERNAME varchar(20) UNIQUE NOT NULL
   Username is kept here
* USER_PASSWORD varchar(255) NOT NULL
   User password is kept here
* PROFILE_PIC varchar(255) NOT NULL
   Profile picture address of user is kept here
* COVER_PIC varchar(255) NOT NULL
   Cover picture address of user is kept here
* MAIL_ADDRESS varchar(50) NOT NULL
   Mail address of user is kept here
* REGISTER_DATE date NOT NULL
   The date which user signed up

In user.py file UserDatabaseOPS class is created and all user related functions are in this class.

*Adding User*
^^^^^^^^^^^^^
This method inserts the new user to database. It takes user columns as parameters.

.. code-block:: python

       def add_user(cls, username, password, profile_picture, cover_picture, mail_address):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO USERS (USERNAME, USER_PASSWORD, PROFILE_PIC, COVER_PIC,
            MAIL_ADDRESS, REGISTER_DATE) VALUES (
                                              %s,
                                              %s,
                                              %s,
                                              %s,
                                              %s,
                                              CURRENT_DATE
                            )"""

            try:
                cursor.execute(query, (username, password, profile_picture,
                                        cover_picture, mail_address))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

*Updating User*
^^^^^^^^^^^^^^^
This method updates the user in database. It takes user columns as parameters.

.. code-block:: python

    def update_user(cls, username, password, profile_picture, cover_picture,
                    mail_address):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Can Altinigne - USERS TABLE ----------------------

            query = """UPDATE USERS SET USER_PASSWORD=%s, PROFILE_PIC=%s,
                          COVER_PIC=%s, MAIL_ADDRESS=%s WHERE USERNAME=%s
                            """

            try:
                cursor.execute(query, (password, profile_picture, cover_picture,
                                mail_address, username))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

*Deleting User*
^^^^^^^^^^^^^^^
This method deletes the user in database. It takes username as parameter.

.. code-block:: python

    def delete_user(cls, username):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Can Altinigne - USERS TABLE ----------------------

            query = """DELETE FROM USERS WHERE USERNAME = %s"""

            try:
                cursor.execute(query, (username,))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

*Selecting User*
^^^^^^^^^^^^^^^^
There are two different ways to select users. Firstly user can be selected by sending user id as parameter. The function
for this purpose is given below.

.. code-block:: python

    def select_user_with_id(cls, user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM USERS WHERE USER_ID=%s"""

            try:
                cursor.execute(query, (user_id,))
                user_data = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            if user_data:
                return User(id=user_data[0], username=user_data[1],
                            password=user_data[2], profile_picture=user_data[3],
                            cover_picture=user_data[4],
                            mail_address=user_data[5], register_date=user_data[6])
            else:
                return -1

Also in the search page a more complex search function is used. This function is named as search_user_for_search and
implementation is shown below. In this function we first find the users that have usernames matched with value. In the
first query we find following numbers with *count()* function and in the second query we find follower numbers for those
users and in the third query we find if we follow those users or not.

.. code-block:: python

    def select_users_for_search(cls, username, current_user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            str = "%{}%".format(username)

            query = """SELECT USERS.USER_ID, USERS.USERNAME, USERS.COVER_PIC,
            USERS.PROFILE_PIC, COUNT(USER_INTERACTION.BASE_USER_ID) FROM USERS
                       INNER JOIN USER_DETAIL ON USERS.USERNAME=USER_DETAIL.USERNAME
                       LEFT JOIN USER_INTERACTION
                       ON USERS.USER_ID=USER_INTERACTION.BASE_USER_ID
                       WHERE USERS.USERNAME LIKE %s
                       GROUP BY
                       USERS.USER_ID, USERS.USERNAME, USERS.COVER_PIC,
                       USERS.PROFILE_PIC, USER_INTERACTION.BASE_USER_ID
                       ORDER BY USERS.USER_ID
                    """

            user_data = []

            try:
                cursor.execute(query, (str,))
                user_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            query = """SELECT COUNT(USER_INTERACTION.TARGET_USER_ID) FROM USERS
                       LEFT JOIN USER_INTERACTION
                       ON USERS.USER_ID=USER_INTERACTION.TARGET_USER_ID
                       WHERE USERS.USERNAME LIKE %s
                       GROUP BY
                       USERS.USERNAME, USER_INTERACTION.TARGET_USER_ID, USERS.USER_ID
                       ORDER BY USERS.USER_ID
                                """

            user_follower_number = []
            followers = []

            try:
                cursor.execute(query, (str,))
                user_follower_number = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            for row in user_follower_number:
                followers.append(row[0])

            query = """SELECT USERS.USER_ID FROM USERS
                       INNER JOIN USER_INTERACTION
                       ON USERS.USER_ID=USER_INTERACTION.TARGET_USER_ID
                       WHERE USER_INTERACTION.BASE_USER_ID=%s
                       AND (USERS.USERNAME LIKE %s)
                    """

            people_that_i_follow = []
            i_followed = []

            try:
                cursor.execute(query, (current_user_id, str))
                people_that_i_follow = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            for row in people_that_i_follow:
                i_followed.append(row[0])

            cursor.close()

            user_list = []
            i = 0

            for row in user_data:

                i_am_following = row[0] in i_followed

                user_list.append(
                    SearchedUser(id=row[0], username=row[1],
                                 follower_number=followers[i],
                                 following_number=row[4], profile_picture=row[3],
                                 cover_picture=row[2], maybe_i_am=i_am_following
                           )
                )

                i+=1

            return user_list

Also in profile page we have three random users to follow on the left side. We find those users by *get_random_users()*
function. It is shown below.

.. code-block:: python

    def get_random_users(cls, user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """ SELECT DISTINCT USERS.PROFILE_PIC, USERS.USERNAME, USERS.USER_ID
            FROM USERS, USER_INTERACTION
                        WHERE USER_ID != %s AND USER_ID
                        NOT IN (SELECT TARGET_USER_ID FROM USER_INTERACTION
                       INNER JOIN USERS ON USERS.USER_ID=USER_INTERACTION.TARGET_USER_ID
                       WHERE USER_INTERACTION.BASE_USER_ID = %s)
                       LIMIT 3
                                    """
            user_list = []
            try:
                cursor.execute(query, (user_id, user_id))
                user_list = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            following = []

            for row in user_list:
                following.append(
                    FollowerOrFollwingUser(username=row[1], profile_pic=row[0],
                    user_id=row[2])
                )

            return following

User Detail Table & Functions
-----------------------------
User Detail Table references to Users Table with username column and references to Cities Table with id column.

The columns of User Detail table are given below.

* USERNAME varchar(20) REFERENCES USERS(USERNAME)
   This column references to Users table
* U_NAME varchar(30) NOT NULL
   Real name of user is kept here
* U_SURNAME varchar(30) NOT NULL
   Real surname of user is kept here
* CITY_ID INTEGER REFERENCES CITIES(CITY_ID)
   This column references to Cities table

In user.py file UserDatabaseOPS class is created and all user detail related functions are in this class.

*Selecting User Detail*
^^^^^^^^^^^^^^^^^^^^^^^
This method selects details for user. It takes username as parameter.

.. code-block:: python

    def select_user_detail(cls, username):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Can Altinigne - USERS TABLE ----------------------

            query = """SELECT USER_DETAIL.*, CITIES.CITY_NAME, CITIES.COUNTRY
            FROM USER_DETAIL
                       INNER JOIN USERS ON USERS.USERNAME=USER_DETAIL.USERNAME
                       INNER JOIN CITIES ON CITIES.CITY_ID=USER_DETAIL.CITY_ID
                       WHERE USER_DETAIL.USERNAME=%s"""
            user_data = 0

            try:
                cursor.execute(query, (username,))
                user_data = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            if user_data and user_data != 0:
                return UserDetails(username=user_data[0], name=user_data[1],
                surname=user_data[2], city=user_data[4], country=user_data[5])
            else:
                return -1

*Adding User Detail*
^^^^^^^^^^^^^^^^^^^^
This method adds details for user. It takes user details as parameters. It works after sign up procedure.

.. code-block:: python

    def add_user_detail(cls, username, real_name, real_surname, city_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Can Altinigne - USERS TABLE ----------------------

            query = """INSERT INTO USER_DETAIL (USERNAME, U_NAME, U_SURNAME, CITY_ID)
            VALUES (
                                                  %s,
                                                  %s,
                                                  %s,
                                                  %s
                                )"""

            try:
                cursor.execute(query, (username, real_name, real_surname, city_id))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

*Updating User Detail*
^^^^^^^^^^^^^^^^^^^^^^
This method updates details for user. It takes user details as parameters. It works in profile page with refresh button
which is under the profile picture.

.. code-block:: python

    def update_user_detail(cls, username, real_name, real_surname, city_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Can Altinigne - USERS TABLE ----------------------

            query = """UPDATE USER_DETAIL SET U_NAME=%s, U_SURNAME=%s, CITY_ID=%s
                              WHERE USERNAME=%s
                                """

            try:
                cursor.execute(query, (real_name, real_surname, city_id, username))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

*Deleting User Detail*
^^^^^^^^^^^^^^^^^^^^^^
This method deletes details for user. It takes username as parameter. It works in profile page with refresh button
which is under the profile picture.

.. code-block:: python

    def delete_user_detail(cls, username):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- Can Altinigne - USERS TABLE ----------------------

            query = """DELETE FROM USER_DETAIL WHERE USERNAME = %s"""

            try:
                cursor.execute(query, (username,))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

Item Table & Functions
----------------------
Item Table references to Currency Table with item currency column.

The columns of Item table are given below.

* ITEM_ID SERIAL PRIMARY KEY UNIQUE NOT NULL
   This column is the serial primary key
* ITEM_NAME varchar(50) NOT NULL
   Item name is kept here
* ITEM_PICTURE varchar(255) NOT NULL
   Picture of item is kept here
* ITEM_PRICE numeric(10,2) NOT NULL
   Item price is kept here
* ITEM_DESCRIPTION text
   Description of item is kept here
* ITEM_CURRENCY varchar(3) REFERENCES CURRENCIES(CURRENCY_NAME)
   Item currency is kept here

In sales.py file SaleDatabaseOPS class is created and all item related functions are in this class.

*Adding Item*
^^^^^^^^^^^^^
This method adds items for a sale. It takes item details as parameters. It works in sales page with add new item button
which is on the left side of page.

.. code-block:: python

    def add_item(cls, item_name, item_picture, item_price, item_description,
                 item_currency):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()


            query = """INSERT INTO
            ITEMS (ITEM_NAME, ITEM_PICTURE, ITEM_PRICE, ITEM_DESCRIPTION, ITEM_CURRENCY)
            VALUES (
                                              %s,
                                              %s,
                                              %s,
                                              %s,
                                              %s
                            )"""

            try:
                cursor.execute(query, (item_name, item_picture, item_price,
                                item_description, item_currency))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

*Selecting Item*
^^^^^^^^^^^^^^^^
There are lots of way of selecting items, since we have many item search ways in sales page. The function shown below
selects item by newest order.

.. code-block:: python

    def select_newest_items(cls, username):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT s.SALE_ID, u.USERNAME, u.PROFILE_PIC, u.MAIL_ADDRESS,
            s.START_DATE, s.END_DATE, i.*, CITIES.CITY_NAME, CITIES.COUNTRY FROM USERS
            AS u
                           INNER JOIN SALES AS s ON s.SELLER_ID=u.USER_ID
                           INNER JOIN ITEMS AS i ON s.ITEM_ID=i.ITEM_ID
                           INNER JOIN CURRENCIES AS c ON i.ITEM_CURRENCY=c.CURRENCY_NAME
                           INNER JOIN CITIES ON s.CITY_ID=CITIES.CITY_ID
                           WHERE u.USERNAME<>%s
                           ORDER BY current_date-s.START_DATE
                           LIMIT 10"""

            user_data = []

            try:
                cursor.execute(query, (username,))
                user_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            sale_list = []

            for row in user_data:
                sale_list.append(
                    Sale(SellerInformation(username=row[1],
                    profile_pic=row[2], mail_address=row[3]), sale_id=row[0],
                         sale_start=row[4], sale_end=row[5],
                         item_info=ItemInformation(item_id=row[6],
                                                   item_name=row[7],
                                                   item_picture=row[8],
                                                   item_price=row[9],
                                                   item_description=row[10],
                                                   item_currency=row[11],
                                                   item_city=row[12],
                                                   item_country=row[13]
                                )
                         )
                )

            return sale_list

The function shown below selects item by currency value.

.. code-block:: python

    def select_items_by_currency(cls, currency, username):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT s.SALE_ID, u.USERNAME, u.PROFILE_PIC, u.MAIL_ADDRESS,
            s.START_DATE, s.END_DATE, i.*, CITIES.CITY_NAME, CITIES.COUNTRY FROM USERS
            AS u
                               INNER JOIN SALES AS s ON s.SELLER_ID=u.USER_ID
                               INNER JOIN ITEMS AS i ON s.ITEM_ID=i.ITEM_ID
                               INNER JOIN CURRENCIES AS c
                               ON i.ITEM_CURRENCY=c.CURRENCY_NAME
                               INNER JOIN CITIES ON s.CITY_ID=CITIES.CITY_ID
                               WHERE c.CURRENCIES=%s AND u.USERNAME<>%s
                               """

            user_data = []

            try:
                cursor.execute(query, (currency, username))
                user_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            sale_list = []

            for row in user_data:
                sale_list.append(
                    Sale(SellerInformation(username=row[1], profile_pic=row[2],
                    mail_address=row[3]), sale_id=row[0],
                         sale_start=row[4], sale_end=row[5],
                         item_info=ItemInformation(item_id=row[6],
                                                   item_name=row[7],
                                                   item_picture=row[8],
                                                   item_price=row[9],
                                                   item_description=row[10],
                                                   item_currency=row[11],
                                                   item_city=row[12],
                                                   item_country=row[13]
                                    )
                         )
                )

            return sale_list

The function shown below selects item by their location.

.. code-block:: python

    def select_items_by_place(cls, city_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT s.SALE_ID, u.USERNAME, u.PROFILE_PIC, u.MAIL_ADDRESS,
            s.START_DATE, s.END_DATE, i.*, CITIES.CITY_NAME, CITIES.COUNTRY FROM USERS 
            AS u
                                   INNER JOIN SALES AS s ON s.SELLER_ID=u.USER_ID
                                   INNER JOIN ITEMS AS i ON s.ITEM_ID=i.ITEM_ID
                                   INNER JOIN CURRENCIES AS c
                                   ON i.ITEM_CURRENCY=c.CURRENCY_NAME
                                   INNER JOIN CITIES ON s.CITY_ID=CITIES.CITY_ID
                                   WHERE CITIES.CITY_ID=%s
                                   """

            user_data = []

            try:
                cursor.execute(query, (city_id,))
                user_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            sale_list = []

            for row in user_data:
                sale_list.append(
                    Sale(SellerInformation(username=row[1], profile_pic=row[2],
                    mail_address=row[3]), sale_id=row[0],
                         sale_start=row[4], sale_end=row[5],
                         item_info=ItemInformation(item_id=row[6],
                                                   item_name=row[7],
                                                   item_picture=row[8],
                                                   item_price=row[9],
                                                   item_description=row[10],
                                                   item_currency=row[11],
                                                   item_city=row[12],
                                                   item_country=row[13]
                                        )
                         )
                )

            return sale_list

The function shown below selects item by their price. It shows items which have a price lower then the user entered.

.. code-block:: python

    def select_items_by_price(cls, username, price, currency):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT s.SALE_ID, u.USERNAME, u.PROFILE_PIC, u.MAIL_ADDRESS,
            s.START_DATE, s.END_DATE, i.*, CITIES.CITY_NAME, CITIES.COUNTRY FROM USERS
            AS u
                                           INNER JOIN SALES AS s
                                           ON s.SELLER_ID=u.USER_ID
                                           INNER JOIN ITEMS AS i ON s.ITEM_ID=i.ITEM_ID
                                           INNER JOIN CURRENCIES AS c
                                           ON i.ITEM_CURRENCY=c.CURRENCY_NAME
                                           INNER JOIN CITIES ON s.CITY_ID=CITIES.CITY_ID
                                           WHERE u.USERNAME<>%s
                                           AND
                                           i.ITEM_PRICE * c.CURRENCY_TO_TL <
                                           %s * (SELECT CURRENCY_TO_TL
                                           FROM CURRENCIES WHERE CURRENCY_NAME=%s)
                                           """

            user_data = []

            try:
                cursor.execute(query, (username, price, currency))
                user_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            sale_list = []

            for row in user_data:
                sale_list.append(
                    Sale(SellerInformation(username=row[1], profile_pic=row[2],
                         mail_address=row[3]), sale_id=row[0],
                         sale_start=row[4], sale_end=row[5],
                         item_info=ItemInformation(item_id=row[6],
                                                   item_name=row[7],
                                                   item_picture=row[8],
                                                   item_price=row[9],
                                                   item_description=row[10],
                                                   item_currency=row[11],
                                                   item_city=row[12],
                                                   item_country=row[13]
                                          )
                         )
                )

            return sale_list

Sale Table & Functions
----------------------
Sale Table is created for Sales page. It references to User Table, Item Table, Cities table.

The columns of Sale table are given below.

* SALE_ID SERIAL PRIMARY KEY
   This column is the serial primary key
* SELLER_ID INTEGER REFERENCES USERS(USER_ID) ON DELETE CASCADE
   Seller id which references to Users table is kept here
* ITEM_ID INTEGER REFERENCES ITEMS(ITEM_ID) ON DELETE CASCADE
   Item id which references to Items table is kept here
* CITY_ID INTEGER REFERENCES CITIES(CITY_ID)
ON DELETE CASCADE ON UPDATE CASCADE
   City id which references to Cities table is kept here
* START_DATE date NOT NULL
   The date that the sale is added
* END_DATE date NOT NULL
   Determined date to end the sale is kept here

In sales.py file SaleDatabaseOPS class is created and all sale related functions are in this class.

*Adding Sale*
^^^^^^^^^^^^^
This method adds sales for a sale. It takes sale details as parameters. It works in sales page with add new item button
which is on the left side of page. First item is added then *add_sale()* function works.

.. code-block:: python

    def add_sale(cls, seller_id, item_id, city_id, end_date):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO SALES (SELLER_ID, ITEM_ID, CITY_ID,
            START_DATE, END_DATE)
            VALUES (
                                              %s,
                                              %s,
                                              %s,
                                              CURRENT_DATE,
                                              %s
                            )"""

            try:
                cursor.execute(query, (seller_id, item_id, city_id, end_date))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

*Delete Sale*
^^^^^^^^^^^^^
This method deletes sales for a sale. It takes sale id as parameter. Since item table references to sale table. When
the sale is deleted, that item is also deleted.

.. code-block:: python

    def delete_sale(cls, sale_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM SALES WHERE SALE_ID = %s"""

            try:
                cursor.execute(query, (sale_id,))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

*Update Sale*
^^^^^^^^^^^^^
This method updates the sale's end date and city id.

.. code-block:: python

    def update_sale(cls, description, end_date, city_id, sale_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """UPDATE SALES SET END_DATE=%s, CITY_ID=%s
                        WHERE SALE_ID=%s"""

            try:
                cursor.execute(query, (description, end_date, city_id, sale_id))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

*Select Sale*
^^^^^^^^^^^^^
This method selects the sale that a user created. It takes the username as parameter and returns the sales of that user.

.. code-block:: python

    def select_sales_of_a_user(cls, username):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT s.SALE_ID, u.USERNAME, u.PROFILE_PIC, u.MAIL_ADDRESS,
            s.START_DATE, s.END_DATE, i.*,
            CITIES.CITY_NAME, CITIES.COUNTRY
                       FROM USERS AS u
                       INNER JOIN SALES AS s ON s.SELLER_ID=u.USER_ID
                       INNER JOIN ITEMS AS i ON s.ITEM_ID=i.ITEM_ID
                       INNER JOIN CURRENCIES AS c ON i.ITEM_CURRENCY=c.CURRENCY_NAME
                       INNER JOIN CITIES ON s.CITY_ID=CITIES.CITY_ID
                       WHERE u.USERNAME=%s"""

            user_data = []

            try:
                cursor.execute(query, (username,))
                user_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            sale_list = []

            for row in user_data:
                sale_list.append(
                    Sale(SellerInformation(username=row[1], profile_pic=row[2],
                         mail_address=row[3]), sale_id=row[0],
                         sale_start=row[4], sale_end=row[5],
                         item_info=ItemInformation(item_id=row[6],
                                                   item_name=row[7],
                                                   item_picture=row[8],
                                                   item_price=row[9],
                                                   item_description=row[10],
                                                   item_currency=row[11],
                                                   item_city=row[12],
                                                   item_country=row[13]
                                        )
                         )
                )

            return sale_list

City Table & Functions
----------------------
City Table is created for Sales page and User page. Add, delete, update and select functions are defined for this table
but actually just select functions are used for web page.

The columns of City table are given below.

* CITY_ID SERIAL PRIMARY KEY
   This column is the serial primary key
* CITY_NAME varchar(50) NOT NULL
   City name is kept here
* DISTANCE_TO_CENTER integer NOT NULL
   This column has a funny story. I was trying to write a item finding function which finds the closest items to users.
   So I give this value to every cities. There is a function named *select_closest_items()* in sales.py.
   I tried to find closest items by benefiting this variable. Then I realized we live on Earth.
   I need at least two coordinates to define specific location. Because I am ashamed, I did not put that function
   in documentation and it was a very sad moment when I realized the situation :)
* COUNTRY varchar(3) NOT NULL
   Country code is kept here

In city.py file CityDatabaseOPS class is created and all city related functions are in this class.

*Select City*
^^^^^^^^^^^^^
This method selects the city with given id. Also after this method, I have a method which returns all cities for login,
signup, sales and profile pages.

.. code-block:: python

    def select_city_by_id(cls, city_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM CITIES WHERE CITY_ID=%s"""

            try:
                cursor.execute(query, (city_id,))
                city_data = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            if city_data:
                return City(city_id=city_data[0], name=city_data[1],
                            distance=city_data[2], country=city_data[3])
            else:
                return -1

The second method which returns all the cities.

.. code-block:: python

    def select_all_cities(cls):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM CITIES"""

            city_data = []

            try:
                cursor.execute(query, ())
                city_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            user_list = []

            for row in city_data:
                user_list.append(
                    City(city_id=row[0], name=row[1], distance=row[2], country=row[3])
                )

            return user_list

Currency Table & Functions
--------------------------
Currency Table is created for sales page. Add, delete, update and select functions are defined for this table
but actually just select functions are used for web page.

The columns of Currency table are given below.

* CURRENCY_NAME varchar(3) PRIMARY KEY UNIQUE NOT NULL
   This column is the primary key and it keeps the code of currency
* CURRENCY_TO_TL numeric(10,2) NOT NULL,
   For comparing different currencies I need to all currencies' comparison to single currency.
* LAST_UPDATE date
   The last day that the currency is updated

In currency.py file CurrencyDatabaseOPS class is created and all city related functions are in this class.

*Select Currency*
^^^^^^^^^^^^^^^^^
This method selects the currency with given name. Also after this method, I have a method which returns all currencies
for Sale page.

.. code-block:: python

    def select_currency(cls, name):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM CURRENCIES WHERE CURRENCY_NAME = %s"""

            try:
                cursor.execute(query, (name,))
                currency_data = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            if currency_data:
                return Currency(name=currency_data[0], to_tl=currency_data[1],
                                date=currency_data[2])
            else:
                return -1

The second method which returns all the currencies.

.. code-block:: python

    def select_all_currencies(cls):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM CURRENCIES"""

            currency_data = []

            try:
                cursor.execute(query, ())
                currency_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            user_list = []

            for row in currency_data:
                user_list.append(
                    Currency(name=row[0], to_tl=row[1], date=row[2])
                )

            return user_list

Other Implementations
---------------------
I have added Bootstrap-Validator JS library for a great-looking form validation by adding this line to layout.html

.. code-block:: javascript

    <script src="https://cdnjs.cloudflare.com/ajax/libs/1000hz-bootstrap-validator/
                0.11.5/validator.min.js"></script>

Also for profile page I use some scripts for navigation bar which user can use for checking followings, followers and
likes.

.. code-block:: javascript

    <script>

        $(document).ready(function () {
            $(".sections").hide();
            $("#knots").show();
            $('.nav-item').removeClass("active");
            $('#li_knot').addClass("active");
        });

        $('#knot_link').click(function (e) {
            $(".sections").hide();
            $("#knots").show();
            $('.nav-item').removeClass("active");
            $('#li_knot').addClass("active");
            e.preventDefault();
            return false;
        });

        $('#follower_link').click(function (e) {
            $(".sections").hide();
            $("#followers").show();
            $('.nav-item').removeClass("active");
            $('#li_follower').addClass("active");
            e.preventDefault();
            return false;
        });

        $('#following_link').click(function (e) {
            $(".sections").hide();
            $("#followings").show();
            $('.nav-item').removeClass("active");
            $('#li_following').addClass("active");
            e.preventDefault();
            return false;
        });

        $('#like_link').click(function (e) {
            $(".sections").hide();
            $("#likes").show();
            $('.nav-item').removeClass("active");
            $('#li_like').addClass("active");
            e.preventDefault();
            return false;
        })

        $('#city_select').on('change', function () {
            var selection = $(this).val();
            $('#city_id').val(selection);
        });

    </script>

For Sales page, I use the scripts below which shows different areas when user selects different search parameters and
choose different currencies for his/her item.

.. code-block:: javascript

    <script>
        $('#search_select').on('change', function () {
            var selection = $(this).val();

            $('#choose_search').val(selection);

            switch (selection) {

                case "price":
                case "username":
                    $(".hid_forms").hide();
                    $("#hid_label").text("Enter the " + selection);
                    $("#otherType").show();
                    if (selection == "price") $("#currencyType").show();
                    break;

                case "currency":
                    $(".hid_forms").hide();
                    $("#currencyType").show();
                    break;

                case "place":
                    $(".hid_forms").hide();
                    $("#placeType").show();
                    break;
                default:
                    $(".hid_forms").hide();
            }
        });

        $('#currency_item').on('change', function () {
            var selection = $(this).val();
            $('#item_change_currency').val(selection);
        });

        $('#my_update_button').on('click', function () {
            var selection = $(this).val();
            $('#item_change_currency').val(selection);
        });

    </script>

In handlers.py file, connecting between database operations and signup page, login page, profile page & sales page is
ensured by me.

For login page in handlers.py file, the function below is defined.

.. code-block:: python

    @site.route('/', methods=['GET', 'POST'])
    def login_page():
        if request.method == 'GET':
            return render_template('login_page.html', signedin=False)
        else:
            if 'Login' in request.form:
                user = UserDatabaseOPS.select_user(request.form['knittername'])

                if user and user != -1:
                    if request.form['knotword'] == user.password:
                        login_user(user)
                        return redirect(url_for('site.user_profile_page',
                                        user_id=user.id))

            return render_template('login_page.html', error=True, signedin=False)

For sign up page in handlers.py file, the function below is defined.

.. code-block:: python

    @site.route('/signup', methods=['GET', 'POST'])
    def signup_page():
        if request.method == 'GET':
            all_cities = CityDatabaseOPS.select_all_cities()
            return render_template('signup_page.html', signedin=False,
                                    cities=all_cities)
        else:
            if 'signup' in request.form:
                user = UserDatabaseOPS.select_user(request.form['knittername'])

                samename = False

                if user and user != -1:
                    if user.username == request.form['knittername']:
                        return render_template('signup_page.html', samename=True)
                else:
                    UserDatabaseOPS.add_user(request.form['knittername'],
                                            request.form['inputPassword'],
                                            request.form['profile_pic'],
                                            request.form['cover_pic'],
                                            request.form['inputEmail'])

                    selected_city_id = request.form['city_id']

                    UserDatabaseOPS.add_user_detail(request.form['knittername'],
                                                    request.form['real_name'],
                                                    request.form['real_surname'],
                                                    selected_city_id)

                return render_template('login_page.html', newly_signup=True,
                                        signedin=False, samename=samename)

For sales page in handlers.py file, the function below is defined.

.. code-block:: python

    @site.route('/knitter_sales/<int:user_id>', methods=['GET', 'POST'])
    @login_required
    def sales_page(user_id):
        user = UserDatabaseOPS.select_user_with_id(user_id)
        _isSearched=False
        if current_user != user:
            abort(403)
        if request.method == 'GET':
            real_name = UserDatabaseOPS.select_user_detail(user.username)
            currency_list = CurrencyDatabaseOPS.select_all_currencies()
            my_city = CityDatabaseOPS.select_city(real_name.city, real_name.country)
            cities = CityDatabaseOPS.select_all_cities()
            my_item_list = SaleDatabaseOPS.select_sales_of_a_user(user.username)

        else:
            _isSearched = True
            if 'add_new_item' in request.form:

                real_name = UserDatabaseOPS.select_user_detail(user.username)
                currency_list = CurrencyDatabaseOPS.select_all_currencies()
                my_city = CityDatabaseOPS.select_city(real_name.city, real_name.country)
                cities = CityDatabaseOPS.select_all_cities()

                SaleDatabaseOPS.add_item(request.form['item_name_form'],
                                         request.form['item_picture_form'],
                                         request.form['item_price_form'],
                                         request.form['item_description_form'],
                                         request.form['item_change_currency'])

                SaleDatabaseOPS.add_sale(user_id,
                            SaleDatabaseOPS.select_new_item_id(
                            request.form['item_name_form'],
                            request.form['item_picture_form'],
                            request.form['item_price_form']),
                            my_city.id, request.form['sale_end_date'])
                my_item_list = SaleDatabaseOPS.select_sales_of_a_user(user.username)

            if 'delete_item' in request.form:
                user = UserDatabaseOPS.select_user_with_id(user_id)
                real_name = UserDatabaseOPS.select_user_detail(user.username)
                currency_list = CurrencyDatabaseOPS.select_all_currencies()
                my_city = CityDatabaseOPS.select_city(real_name.city, real_name.country)
                cities = CityDatabaseOPS.select_all_cities()

                SaleDatabaseOPS.delete_sale(request.form['delete_this_sale'])

                my_item_list = SaleDatabaseOPS.select_sales_of_a_user(user.username)

            if 'search_item' in request.form:
                user = UserDatabaseOPS.select_user_with_id(user_id)
                real_name = UserDatabaseOPS.select_user_detail(user.username)
                currency_list = CurrencyDatabaseOPS.select_all_currencies()
                my_city = CityDatabaseOPS.select_city(real_name.city, real_name.country)
                cities = CityDatabaseOPS.select_all_cities()
                my_item_list = 1

                if request.form['choose_search'] == 'username':
                    my_item_list = SaleDatabaseOPS.select_sales_of_a_user(
                    request.form['keyword'])
                elif request.form['choose_search'] == 'closest':
                    my_item_list = SaleDatabaseOPS.select_closest_items(user.username,
                                                                        my_city.id)
                elif request.form['choose_search'] == 'price':
                    my_item_list = SaleDatabaseOPS.select_items_by_price(user.username,
                                                               request.form['keyword'],
                    request.form['currency_select'])
                elif request.form['choose_search'] == 'currency':
                    my_item_list = SaleDatabaseOPS.select_items_by_currency(
                                                        request.form['currency_select'],
                                                        user.username)
                elif request.form['choose_search'] == 'place':
                    my_item_list = SaleDatabaseOPS.select_items_by_place(
                                                            request.form['city_select'])
                elif request.form['choose_search'] == 'newest':
                    my_item_list = SaleDatabaseOPS.select_newest_items(user.username)


        return render_template('sales_knitter.html', signedin=True, user=user,
                                    real_name=real_name, my_city=my_city, cities=cities,
                                    currency_list=currency_list,
                                    my_item_list=my_item_list, isSearched=_isSearched)

For profile page in handlers.py file, the function below is defined.

.. code-block:: python

    @site.route('/user_profile/<int:user_id>', methods=['GET', 'POST'])
    @login_required
    def user_profile_page(user_id):
        user = UserDatabaseOPS.select_user_with_id(user_id)
        if user is -1:
            abort(404)
        user_check = True
        if current_user != user:
            user_check = False
        if request.method == 'GET':
            real_name = UserDatabaseOPS.select_user_detail(user.username)
            my_city = CityDatabaseOPS.select_city(real_name.city, real_name.country)
            cities = CityDatabaseOPS.select_all_cities()
            knot_list = KnotDatabaseOPS.select_knots_for_owner(user.id)
            like_list = KnotDatabaseOPS.get_likes(user.id)
            followers = UserDatabaseOPS.get_followers(user.id)
            followings = UserDatabaseOPS.get_following(user.id)
            lengths = {'knot_len': len(knot_list), 'like_len': len(like_list),
                        'followers_len': len(followers),
                       'followings_len': len(followings)}
            random_users = UserDatabaseOPS.get_random_users(current_user.id)
            return render_template('user_profile.html', signedin=True, user=user,
                                   real_name=real_name, my_city=my_city, cities=cities,
                                   knot_list=knot_list, user_check=user_check,
                                   likes=like_list, followers=followers,
                                   followings=followings, lengths=lengths,
                                   random=random_users)
        else:
            if 'changeImage' in request.form:
                user.profile_pic = request.form['imageURL']
                my_name = request.form['my_name']
                my_surname = request.form['my_surname']
                user.cover_pic = request.form['coverURL']
                city_id = request.form['city_id']
                cities = CityDatabaseOPS.select_all_cities()

                real_name = UserDatabaseOPS.select_user_detail(user.username)

                if real_name == -1:
                    UserDatabaseOPS.add_user_detail(user.username, my_name, my_surname,
                    city_id)
                else:
                    UserDatabaseOPS.update_user_detail(user.username, my_name,
                    my_surname, city_id)

                UserDatabaseOPS.update_user(user.username, user.password,
                                            user.profile_pic, user.cover_pic,
                                            user.mail_address)

                real_name = UserDatabaseOPS.select_user_detail(user.username)
                my_city = CityDatabaseOPS.select_city(real_name.city, real_name.country)
                knot_list = KnotDatabaseOPS.select_knots_for_owner(user.id)
                like_list = KnotDatabaseOPS.get_likes(user_id)
                followers = UserDatabaseOPS.get_followers(user_id)
                followings = UserDatabaseOPS.get_following(user_id)
                lengths = {'knot_len': len(knot_list), 'like_len': len(like_list),
                            'followers_len': len(followers),
                           'followings_len': len(followings)}
                random_users = UserDatabaseOPS.get_random_users(current_user.id)

            if 'deleteReal' in request.form:
                user = UserDatabaseOPS.select_user_with_id(user_id)
                cities = CityDatabaseOPS.select_all_cities()
                UserDatabaseOPS.delete_user_detail(user.username)
                real_name = UserDatabaseOPS.select_user_detail(user.username)
                my_city = CityDatabaseOPS.select_city(real_name.city, real_name.country)
                knot_list = KnotDatabaseOPS.select_knots_for_owner(user.id)
                like_list = KnotDatabaseOPS.get_likes(user.id)
                followers = UserDatabaseOPS.get_followers(user.id)
                followings = UserDatabaseOPS.get_following(user.id)
                lengths = {'knot_len': len(knot_list), 'like_len': len(like_list),
                           'followers_len': len(followers),
                           'followings_len': len(followings)}
                random_users = UserDatabaseOPS.get_random_users(current_user.id)

            if 'follow' in request.form:
                user = UserDatabaseOPS.select_user_with_id(user_id)
                target_user = request.form['target_user']
                cities = CityDatabaseOPS.select_all_cities()
                UserDatabaseOPS.follow(user_id, target_user)
                real_name = UserDatabaseOPS.select_user_detail(user.username)
                my_city = CityDatabaseOPS.select_city(real_name.city, real_name.country)
                knot_list = KnotDatabaseOPS.select_knots_for_owner(user.id)
                like_list = KnotDatabaseOPS.get_likes(user.id)
                followers = UserDatabaseOPS.get_followers(user.id)
                followings = UserDatabaseOPS.get_following(user.id)
                lengths = {'knot_len': len(knot_list), 'like_len': len(like_list),
                           'followers_len': len(followers),
                           'followings_len': len(followings)}
                random_users = UserDatabaseOPS.get_random_users(current_user.id)

            return render_template('user_profile.html', signedin=True, user=user,
                                   real_name=real_name,
                                   my_city=my_city, cities=cities, knot_list=knot_list,
                                   user_check=user_check,
                                   likes=like_list, followers=followers,
                                   followings=followings, lengths=lengths,
                                   random=random_users
                                   )
