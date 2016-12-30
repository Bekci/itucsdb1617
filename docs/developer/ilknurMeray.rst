Parts Implemented by İlknur Meray
=================================

I implemented shelf, book and quote entities, also I created USER_INTERACTION, SHELF, BOOK and QUOTE tables.
I created classes for every table and these table's database operations. Additionally, I implemented home page and books page of the Knitter.

USER_INTERACTION Table and Operations
-------------------------------------

USER_INTERACTION table is used to hold following/follower relation between users. Table's columns are

1. BASE_USER_ID

- Its type is integer and it references USERS table.

- It is used to hold current user's id.

2. TARGET_USER_ID

- Its type is integer and it references USERS table.

- It is used to hold user's id who is followed by current user.


**Query for creating USER_INTERACTION table**

.. code-block:: python

    query = """CREATE TABLE IF NOT EXISTS USER_INTERACTION(
                        BASE_USER_ID INTEGER REFERENCES USERS(USER_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                        TARGET_USER_ID INTEGER REFERENCES USERS(USER_ID) ON DELETE CASCADE ON UPDATE CASCADE
                    )"""


**add_user_interaction Method**

This method adds a row to USER_INTERACTION table which includes the information of current user's id and her/his followed user's id.

.. code-block:: python

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


**delete_user_interaction Method**

This method deletes a row from USER_INTERACTION table when current user unfollows the other user.

.. code-block:: python

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


**select_followings_from_user_interaction Method**

This method selects the followings' id from USER_INTERACTION table.

.. code-block:: python

    def select_followings_from_user_interaction(cls, base_id):  # base id keeps followers
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - USER_INTERACTION TABLE -----------------------

            query = """SELECT TARGET_USER_ID FROM USER_INTERACTION WHERE BASE_USER_ID = %s"""
            followings_ids = []
            # followings_list = []
            try:
                cursor.execute(query, (base_id,))
                followings_ids = cursor.fetchall()
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            return followings_ids


**select_followers_from_user_interaction Method**

This method selects the followers' id from USER_INTERACTION table.

.. code-block:: python

    def select_followers_from_user_interaction(cls, target_id):  # target_id keeps followings
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - USER_INTERACTION TABLE -----------------------

            query = """SELECT BASE_USER_ID FROM USER_INTERACTION WHERE TARGET_USER_ID = %s"""
            followers_ids = []
            # followers_list = []

            try:
                cursor.execute(query, (target_id,))
                followers_ids = cursor.fetchall()
            except dbapi2.IntegrityError:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            return followers_ids


**select_interactions_for_search Method**

This method selects the current user's followings and followers from USER_INTERACTION table.

.. code-block:: python

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


*Why there is no update operation for USER_INTERACTION table?*

An update operation can not be performed on USER_INTERACTION table.
When a base user unfollows another target user, that means, there is no interaction between each other and it requires a delete operation.
Also, when a base user follows another target user, that requires an insert operation because of the follow interaction between users.
As a result of that, any record in USER_INTERACTION table is not updated for follow/unfollow operations.


SHELF Table and Operations
--------------------------

SHELF table is used to store user's shelf. Its columns are:


1. SHELF_ID

- It is serial number which is generated automatically and primary key of the table.

- It is used to hold shelf's id.

2. SHELF_NAME

- Its type is varchar(50) and it is unique, at the same time it can not be null.

- It holds the shelf's name.

3. IS_MAIN

- Its type is boolean.

- It is used while detecting whether the shelf will be the user's first shelf or not. If its value equals to true, it means shelf will be first shelf on the bookshelf. On the other hand, it it is equals to false, shelf will not located to first shelf on the bookshelf.

4. BOOK_COUNTER

- Its type is integer and when a new shelf is created there is no book within this shelf so its book counter will be 0 as default.

- It holds the number of books inside the shelf.

5. SHELF_USER_ID

- Its type is integer and it references USERS table.

- It holds the shelf's owner id.


**Query for creating SHELF table**

.. code-block:: python

    query = """CREATE TABLE IF NOT EXISTS SHELF(
                            SHELF_ID SERIAL PRIMARY KEY,
                            SHELF_NAME VARCHAR(50) UNIQUE NOT NULL,
                            IS_MAIN BOOLEAN,
                            BOOK_COUNTER INTEGER DEFAULT 0,
                            SHELF_USER_ID INTEGER REFERENCES USERS(USER_ID) ON DELETE CASCADE ON UPDATE CASCADE
                    )"""


**add_shelf Method**

This method adds new shelf to SHELF table. It takes new shelf's information as parameter.

.. code-block:: python

    def add_shelf(cls, shelf_name, is_main, shelf_user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            book_counter = 0
            # ----------- ilknur Meray - SHELF TABLE -----------------------

            query = """INSERT INTO SHELF (SHELF_NAME, IS_MAIN, BOOK_COUNTER, SHELF_USER_ID) VALUES (
                                                %s,
                                                %s,
                                                %s,
                                                %s
                        )"""

            try:
                cursor.execute(query, (shelf_name, is_main, book_counter, shelf_user_id))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()


**update_shelf_name Method**

This method is used to update shelf's name. shelf_id and new_shelf_name parameters come via form attribute in html file of books_page.

.. code-block:: python

    def update_shelf_name(cls, shelf_id, new_shelf_name):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - SHELF TABLE -----------------------

            query = """UPDATE SHELF SET SHELF_NAME = %s WHERE SHELF_ID = %s"""

            try:
                cursor.execute(query, (new_shelf_name, shelf_id))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()


**update_main_shelf Method**

This method is used to update first shelf of the bookcase.

.. code-block:: python

    def update_main_shelf(cls, shelf_id, is_main):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - SHELF TABLE -----------------------
            if is_main:
                query = """UPDATE SHELF SET IS_MAIN = %s WHERE SHELF_ID = %s"""

                try:
                    cursor.execute(query, (is_main, shelf_id,))
                except dbapi2.Error:
                    connection.rollback()
                else:
                    connection.commit()

                cursor.close()

                cursor = connection.cursor()
                query = """UPDATE SHELF SET IS_MAIN = FALSE WHERE SHELF_ID <> %s"""

                try:
                    cursor.execute(query, (shelf_id,))
                except dbapi2.Error:
                    connection.rollback()
                else:
                    connection.commit()

                cursor.close()
            else:
                query = """UPDATE SHELF SET IS_MAIN = %s WHERE SHELF_ID = %s"""

                try:
                    cursor.execute(query, (is_main, shelf_id,))
                except dbapi2.Error:
                    connection.rollback()
                else:
                    connection.commit()

                cursor.close()

                cursor = connection.cursor()
                query = """UPDATE SHELF SET IS_MAIN = TRUE WHERE SHELF_ID <> %s"""

                try:
                    cursor.execute(query, (shelf_id,))
                except dbapi2.Error:
                    connection.rollback()
                else:
                    connection.commit()

                cursor.close()


**delete_shelf Method**

This method deletes shelf with given id from bookcase.

.. code-block:: python

    def delete_shelf(cls, shelf_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - SHELF TABLE -----------------------

            query = """DELETE FROM SHELF WHERE SHELF_ID = %s"""

            try:
                cursor.execute(query, (shelf_id,))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()


**select_shelves Method**

This method selects the shelves of bookcase. It sorts taken shelfs again, if one shelf's is_main value is true.

.. code-block:: python

    def select_shelves(cls, shelf_user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - SHELF TABLE -----------------------

            query = """SELECT * FROM SHELF WHERE SHELF_USER_ID = %s"""

            shelf_data = []
            try:
                cursor.execute(query, (shelf_user_id,))
                shelf_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            shelf_list = []

            for element in shelf_data:
                shelf_list.append(
                    Shelf(shelf_id=element[0], shelf_name=element[1], is_main=element[2], book_counter=element[3], shelf_user_id=element[4]))

            for j in shelf_list:
                if j.is_main:
                    a, b = shelf_list.index(j), 0
                    shelf_list[b], shelf_list[a] = shelf_list[a], shelf_list[b]

            return shelf_list


**increase_book_counter Method**

This method increases book_counter value of the shelf with given id when a new book is added to this shelf.

.. code-block:: python

    def increase_book_counter(cls, shelf_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - SHELF TABLE -----------------------

            query = """UPDATE SHELF SET BOOK_COUNTER = BOOK_COUNTER+1 WHERE SHELF_ID = %s"""

            try:
                cursor.execute(query, (shelf_id,))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()


**decrease_book_counter Method**

This method decreases book_counter value of the shelf with given id when a book is deleted from this shelf.

.. code-block:: python

    def decrease_book_counter(cls, shelf_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - SHELF TABLE -----------------------

            query = """UPDATE SHELF SET BOOK_COUNTER = BOOK_COUNTER-1 WHERE SHELF_ID = %s"""

            try:
                cursor.execute(query, (shelf_id,))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()


BOOK Table and Operations
-------------------------

BOOK table is used to store user's books. Its columns are:


1. BOOK_ID

- It is serial primary key, so it is generated automatically.

- It holds book's id.

2. BOOK_TITLE

- Its type is varchar(50) and it can not be NULL.

- It holds book's title.

3. BOOK_COVER

- Its type is varchar(255) and it can not be NULL.

- It holds book's cover picture's URL.

4. BOOK_WRITER

- Its type is varchar(50) and it can not be NULL.

- It holds book's author's name and surname.

5. BOOK_GENRE

- Its type is varchar(50) and it can not be NULL.

- It holds book's genre.

6. DATE_READ

- Its type is date and it can not be NULL.

- It holds book's read date.

7. USER_RATE

- Its type is integer and 0 as default because when table is created, there is no book to rate.

- It holds user's rate about book from 1 to 5.

8. BOOK_REVIEW

- Its type is text.

- It is used for user's comments about book.

9. BOOK_SHELF_ID

- Its type is integer and it references SHELF table.

- It holds shelf_id of book.

10. BOOK_READER_ID

- Its type is integer and it references USERS table.

- It holds user_id of book.


**Query for creating the BOOK table**


.. code-block:: python

    query = """CREATE TABLE IF NOT EXISTS BOOK(
                            BOOK_ID SERIAL PRIMARY KEY,
                            BOOK_TITLE VARCHAR(50) NOT NULL,
                            BOOK_COVER VARCHAR(255) NOT NULL,
                            BOOK_WRITER VARCHAR(50) NOT NULL,
                            BOOK_GENRE VARCHAR(50) NOT NULL,
                            DATE_READ DATE NOT NULL,
                            USER_RATE INTEGER DEFAULT 0,
                            BOOK_REVIEW TEXT,
                            BOOK_SHELF_ID INTEGER REFERENCES SHELF(SHELF_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                            BOOK_READER_ID INTEGER REFERENCES USERS(USER_ID) ON DELETE CASCADE ON UPDATE CASCADE
                    )"""


**add_book Method**

This method used to add new book to shelf with given id. New book's all information are sent as parameters to this function.
This will increase the book_cunter of the shelf since a new book is added.


.. code-block:: python

    def add_book(cls, book_title, book_cover, book_writer, book_genre, date_read, user_rate, book_review, book_shelf, book_reader_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - BOOK TABLE -----------------------

            query = """INSERT INTO BOOK (BOOK_TITLE, BOOK_COVER, BOOK_WRITER, BOOK_GENRE, DATE_READ, USER_RATE, BOOK_REVIEW, BOOK_SHELF_ID, BOOK_READER_ID) VALUES (
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s,
                                                %s
                        )"""

            try:
                cursor.execute(query, (book_title, book_cover, book_writer, book_genre, date_read, user_rate, book_review, book_shelf, book_reader_id))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()
            ShelfDatabaseOPS.increase_book_counter(book_shelf)


**update_book Method**

This method used to update book with given book_id and user_id. Book's all information are sent as parameters to this function for update operation.

.. code-block:: python

    def update_book(cls, book_id, book_title, book_cover, book_writer, book_genre, date_read, user_rate, book_review, book_shelf, book_reader_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - BOOK TABLE -----------------------

            query = """UPDATE BOOK SET BOOK_TITLE=%s,
                                    BOOK_COVER = %s,
                                    BOOK_WRITER = %s,
                                    BOOK_GENRE = %s,
                                    DATE_READ = %s,
                                    USER_RATE = %s,
                                    BOOK_REVIEW = %s,
                                    BOOK_SHELF_ID = %s WHERE BOOK_ID = %s AND BOOK_READER_ID = %s"""

            try:
                cursor.execute(query, (book_title, book_cover, book_writer, book_genre, date_read, user_rate, book_review, book_shelf, book_id, book_reader_id))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()


**find_shelf_from_id Method**

This method is used to find shelf of the book with given id.

.. code-block:: python

    def find_shelf_from_id(cls, book_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - BOOK TABLE -----------------------

            query = """SELECT BOOK_SHELF_ID FROM BOOK WHERE BOOK_ID=%s"""

            try:
                cursor.execute(query, (book_id,))
                book_data = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            return book_data


**delete_book Method**

This method deletes the book with given id from BOOK table.

.. code-block:: python

    def delete_book(cls, book_id):
        shelf_id = BookDatabaseOPS.find_shelf_from_id(book_id)
        ShelfDatabaseOPS.decrease_book_counter(shelf_id)
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - BOOK TABLE -----------------------

            query = """DELETE FROM BOOK WHERE BOOK_ID = %s"""

            try:
                cursor.execute(query, (book_id,))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()


**select_all_books_of_user Method**

When books page is opened first, all books should be viewed, so this function is used for select all booksof the user with given id in the all shelves.

.. code-block:: python

    def select_all_books_of_user(cls, book_reader_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - BOOK TABLE -----------------------

            query = """SELECT * FROM BOOK WHERE BOOK_READER_ID=%s ORDER BY USER_RATE DESC"""

            book_data = []

            try:
                cursor.execute(query, (book_reader_id,))
                book_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            book_list = []

            for element in book_data:
                book_list.append(
                    Book(book_id=element[0], book_title=element[1], book_cover=element[2], book_writer=element[3], book_genre=element[4],
                         date_read=element[5], user_rate=element[6], book_review=element[7], book_shelf=element[8], book_reader_id=element[9]))

            return book_list


**select_books_from_shelf Method**

When user clicks to a specific shelf, all books in this shelf is shown, so this function is used for selecting all books of user with given id in the specified shelf.

.. code-block:: python

    def select_books_from_shelf(cls, book_shelf, book_reader_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - BOOK TABLE -----------------------
            query = """SELECT * FROM BOOK WHERE BOOK_SHELF_ID=%s AND BOOK_READER_ID = %s"""

            book_data = []

            try:
                cursor.execute(query, (book_shelf, book_reader_id))
                book_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            book_list = []

            for element in book_data:
                book_list.append(
                    Book(book_id=element[0], book_title=element[1], book_cover=element[2], book_writer=element[3], book_genre=element[4],
                         date_read=element[5], user_rate=element[6], book_review=element[7], book_shelf=element[8], book_reader_id=element[9]))

            return book_list


QUOTE Table and Operations
--------------------------

QUOTE table is used to store quotes which are chosen from the user's books by user. Its columns are:


1. QUOTE_ID

- It is serial primary key, so it is incremented automatically.

- It holds quote's id.

2. QUOTE_CONTENT

- Its type is text and it can not be NULL.

- It stores the quote content.

3. QUOTE_BOOK_ID

- Its type is integer and it references BOOK table.

- It is used for determining the book that the quote is taken from.

4. QUOTE_USER_ID

- Its type is integer and it references USERS table.

- It holds the user id who quoted something from the books.


**Query for creating QUOTE table**


.. code-block:: python

    query = """CREATE TABLE IF NOT EXISTS QUOTE(
                            QUOTE_ID SERIAL PRIMARY KEY,
                            QUOTE_CONTENT TEXT NOT NULL,
                            QUOTED_BOOK_ID INTEGER REFERENCES BOOK(BOOK_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                            QUOTE_USER_ID INTEGER REFERENCES USERS(USER_ID) ON DELETE CASCADE ON UPDATE CASCADE
                    )"""


**add_quote Method**

This method adds quote to QUOTE table and new quote's information are sent as parameter.


.. code-block:: python

    def add_quote(cls, quote_content, quoted_book_id, quote_user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            # ----------- ilknur Meray - QUOTE TABLE -----------------------

            query = """INSERT INTO QUOTE (QUOTE_CONTENT, QUOTED_BOOK_ID, QUOTE_USER_ID) VALUES (
                                                %s,
                                                %s,
                                                %s
                        )"""

            try:
                cursor.execute(query, (quote_content, quoted_book_id, quote_user_id))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

**update_quote Method**

This method updates quote in QUOTE table and quote's updated information are sent as parameter.


.. code-block:: python

    def update_quote(cls, quote_id, new_quote_content, new_quoted_book):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - QUOTE TABLE -----------------------

            query = """UPDATE QUOTE SET QUOTE_CONTENT = %s,
                                        QUOTED_BOOK_ID = %s WHERE QUOTE_ID = %s"""

            try:
                cursor.execute(query, (new_quote_content, new_quoted_book, quote_id))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

**delete_quote Method**

This method deletes quote with given id from QUOTE table.


.. code-block:: python

    def delete_quote(cls, quote_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - QUOTE TABLE -----------------------

            query = """DELETE FROM QUOTE WHERE QUOTE_ID = %s"""

            try:
                cursor.execute(query, (quote_id,))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

**select_quotes Method**

This method selects quotes of user with given user id from QUOTE table.


.. code-block:: python

    def select_quotes(cls, quote_user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            # ----------- ilknur Meray - QUOTE TABLE -----------------------

            query = """SELECT q.QUOTE_ID, q.QUOTE_CONTENT, q.QUOTED_BOOK_ID, q.QUOTE_USER_ID, b.BOOK_TITLE
                        FROM QUOTE AS q LEFT JOIN BOOK AS b ON q.QUOTED_BOOK_ID = b.BOOK_ID WHERE q.QUOTE_USER_ID = %s"""

            quote_data = []
            try:
                cursor.execute(query, (quote_user_id,))
                quote_data = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            quote_list = []

            for element in quote_data:
                quote_list.append(
                    Quote(quote_id=element[0], quote_content=element[1], quoted_book_id=element[2], quote_user_id=element[3], book_name=element[4]))

            return quote_list

Pages of Knitter
----------------

I implemented home page and books page for Knitter.

Function for Home Page in handlers.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. code-block:: python

    @site.route('/home/<int:user_id>', methods=['GET', 'POST'])
    @login_required
    def home_page(user_id):
        user = UserDatabaseOPS.select_user_with_id(user_id)
        if current_user != user:
            abort(403)
        real_name = UserDatabaseOPS.select_user_detail(user.username)
        if request.method == 'GET':
            my_followings_id = InteractionDatabaseOPS.select_followings_from_user_interaction(user.id)
            my_followings_user = []
            my_followings_user.append(user)
            my_followings_knots = []
            my_temp_knot_list = KnotDatabaseOPS.select_knots_for_owner(user.id)
            new_groups= GroupDatabaseOPS.find_groups()
            for counter in my_temp_knot_list:
                my_followings_knots.append(counter)
            for index in my_followings_id:
                my_followings_user.append(UserDatabaseOPS.select_user_with_id(index))
                temp_knot_list = KnotDatabaseOPS.select_knots_for_owner(index)
                for element in temp_knot_list:
                    my_followings_knots.append(element)
            return render_template('home_page.html', signedin=True, user=user, real_name=real_name, my_followings_knots=my_followings_knots, my_followings_user=my_followings_user, new_groups=new_groups)
        else:
            if 'add_knot' in request.form:
                KnotDatabaseOPS.add_knot(user_id, request.form['new_knot_content'], 0, 0, False, datetime.now().date().isoformat())
                return redirect(url_for('site.home_page', user_id=user.id))
            elif 'delete' in request.form:
                KnotDatabaseOPS.delete_knot(request.form['delete'])
                return redirect(url_for('site.home_page', user_id=user.id))
            elif 'update_knot' in request.form:
                KnotDatabaseOPS.update_knot(user.id, request.form['update_knot_content'], 0, 0, False, datetime.now().date().isoformat(), request.form['update_knot'])
                return redirect(url_for('site.home_page', user_id=user.id))
            elif 'search' in request.form:
                query = request.form['search_bar']
                print(query)
                return redirect(url_for('site.search_page', user_id=user.id, query=query))
            elif 'like' in request.form:
                is_like = NotificationDatabaseOPS.check_like(request.form['like'], user.id, True)
                if is_like:
                    NotificationDatabaseOPS.delete_relation(request.form['like'], user.id, True)
                    NotificationDatabaseOPS.decrease_knot_like(request.form['like'])
                else:
                    NotificationDatabaseOPS.insert_relation(request.form['like'], user.id, True)
                    NotificationDatabaseOPS.increase_knot_like(request.form['like'])
                return redirect(url_for('site.home_page', user_id=user.id))
                elif 'reknot' in request.form:
                is_reknot = NotificationDatabaseOPS.check_reknot(request.form['reknot'], user.id, False)
                if is_reknot:
                    NotificationDatabaseOPS.delete_relation(request.form['reknot'], user.id, False)
                    NotificationDatabaseOPS.decrease_knot_reknot(request.form['reknot'])
                else:
                    NotificationDatabaseOPS.insert_relation(request.form['reknot'], user.id, False)
                    NotificationDatabaseOPS.increase_knot_reknot(request.form['reknot'])
                return redirect(url_for('site.home_page', user_id=user.id))


    @site.route('/home/knots/<int:user_id>', methods=['GET', 'POST'])
    @login_required
    def home_page_knots(user_id):
        user = UserDatabaseOPS.select_user_with_id(user_id)
        if current_user != user:
            abort(403)
        return render_template('home_page.html', signedin=True, user=user)


Function for Books Page in handlers.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. code-block:: python

    @site.route('/books_page/<int:user_id>', methods=['GET', 'POST'])
    @login_required
    def books_page(user_id):
        user = UserDatabaseOPS.select_user_with_id(user_id)
        if current_user != user:
            abort(403)
        real_name = UserDatabaseOPS.select_user_detail(user.username)
        if request.method == 'GET':
            my_shelves = ShelfDatabaseOPS.select_shelves(user_id)
            my_books = []
            my_quotes = []
            my_books = BookDatabaseOPS.select_all_books_of_user(user_id)
            my_quotes = QuoteDatabaseOPS.select_quotes(user_id)
            return render_template('books_page.html', signedin=True, user=user, real_name=real_name, my_shelves=my_shelves, my_books=my_books, my_quotes=my_quotes)
        else:
            if 'add_shelf' in request.form:
                ShelfDatabaseOPS.add_shelf(request.form['shelf_name'], request.form['first_shelf'], user_id)
                return redirect(url_for('site.books_page', user_id=user.id))
            elif 'delete_shelf' in request.form:
                ShelfDatabaseOPS.delete_shelf(request.form['delete_shelf'])
                return redirect(url_for('site.books_page', user_id=user.id))
            elif 'update_shelf' in request.form:
                ShelfDatabaseOPS.update_shelf_name(request.form['update_shelf'], request.form['updated_shelf_name'])
                ShelfDatabaseOPS.update_main_shelf(request.form['update_shelf'], request.form['updated_first_shelf'])
                return redirect(url_for('site.books_page', user_id=user.id))
            elif 'add_book' in request.form:
                BookDatabaseOPS.add_book(request.form['book_title'], request.form['book_cover'], request.form['book_writer'], request.form['book_genre'],
                                        request.form['date_read'], request.form['user_rate'],request.form['book_review'], request.form['add_book'],
                                        user_id)
                return redirect(url_for('site.books_page', user_id=user.id))
            elif 'delete_book' in request.form:
                BookDatabaseOPS.delete_book(request.form['delete_book'])
                return redirect(url_for('site.books_page', user_id=user.id))
            elif 'update_book' in request.form:
                BookDatabaseOPS.update_book(request.form['update_book'], request.form['updated_book_title'], request.form['updated_book_cover'],
                                            request.form['updated_book_writer'], request.form['updated_book_genre'],
                                            request.form['updated_date_read'], request.form['updated_user_rate'], request.form['updated_book_review'],
                                            request.form['updated_book_shelf'], user_id)
                return redirect(url_for('site.books_page', user_id=user.id))
            elif 'add_quote' in request.form:
                QuoteDatabaseOPS.add_quote(request.form['quote_content'], request.form['quoted_book'], user_id)
                return redirect(url_for('site.books_page', user_id=user.id))
            elif 'delete_quote' in request.form:
                QuoteDatabaseOPS.delete_quote(request.form['delete_quote'])
                return redirect(url_for('site.books_page', user_id=user.id))
            elif 'update_quote' in request.form:
                QuoteDatabaseOPS.update_quote(request.form['update_quote'], request.form['updated_quote_content'], request.form['updated_quote_book'])
                return redirect(url_for('site.books_page', user_id=user.id))


    @site.route('/books_page/<int:user_id>/<int:shelf_id>', methods=['GET', 'POST'])
    @login_required
    def shelf_books_page(user_id, shelf_id):
        user = UserDatabaseOPS.select_user_with_id(user_id)
        if current_user != user:
            abort(403)
        real_name = UserDatabaseOPS.select_user_detail(user.username)
        if request.method == 'GET':
            my_shelves = ShelfDatabaseOPS.select_shelves(user_id)
            my_books = []
            my_quotes = []
            my_books = BookDatabaseOPS.select_books_from_shelf(shelf_id, user_id)
            my_quotes = QuoteDatabaseOPS.select_quotes(user_id)
            return render_template('books_page.html', signedin=True, user=user, real_name=real_name, my_shelves=my_shelves, my_books=my_books, my_quotes=my_quotes)
        else:
            if 'add_shelf' in request.form:
                ShelfDatabaseOPS.add_shelf(request.form['shelf_name'], request.form['first_shelf'], user_id)
                return redirect(url_for('site.books_page', user_id=user.id))
            elif 'delete_shelf' in request.form:
                ShelfDatabaseOPS.delete_shelf(request.form['delete_shelf'])
                return redirect(url_for('site.books_page', user_id=user.id))
            elif 'update_shelf' in request.form:
                ShelfDatabaseOPS.update_shelf_name(request.form['update_shelf'], request.form['updated_shelf_name'])
                ShelfDatabaseOPS.update_main_shelf(request.form['update_shelf'], request.form['updated_first_shelf'])
                return redirect(url_for('site.books_page', user_id=user.id))
            elif 'add_book' in request.form:
                BookDatabaseOPS.add_book(request.form['book_title'], request.form['book_cover'], request.form['book_writer'], request.form['book_genre'],
                                        request.form['date_read'], request.form['user_rate'],request.form['book_review'], request.form['add_book'],
                                        user_id)
                return redirect(url_for('site.books_page', user_id=user.id))
            elif 'delete_book' in request.form:
                BookDatabaseOPS.delete_book(request.form['delete_book'])
                return redirect(url_for('site.books_page', user_id=user.id))
            elif 'update_book' in request.form:
                BookDatabaseOPS.update_book(request.form['update_book'], request.form['updated_book_title'], request.form['updated_book_cover'],
                                            request.form['updated_book_writer'], request.form['updated_book_genre'],
                                            request.form['updated_date_read'], request.form['updated_user_rate'], request.form['updated_book_review'],
                                            request.form['updated_book_shelf'], user_id)
                return redirect(url_for('site.books_page', user_id=user.id))
            elif 'add_quote' in request.form:
                QuoteDatabaseOPS.add_quote(request.form['quote_content'], request.form['quoted_book'], user_id)
                return redirect(url_for('site.books_page', user_id=user.id))
            elif 'delete_quote' in request.form:
                QuoteDatabaseOPS.delete_quote(request.form['delete_quote'])
                return redirect(url_for('site.books_page', user_id=user.id))
            elif 'update_quote' in request.form:
                QuoteDatabaseOPS.update_quote(request.form['update_quote'], request.form['updated_quote_content'], request.form['updated_quote_book'])
                return redirect(url_for('site.books_page', user_id=user.id))
