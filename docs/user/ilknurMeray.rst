Parts Implemented by İlknur Meray
=================================

Home Page
---------

Home page is the main page of the Knitter where users can knot, see their own knots and followings' knots besides viewing existing groups and their descriptions.
Moreover, user can open his/her online library page and last added groups' page from the home page.
The home page consists of three parts:
1. Summary of user's information on the left hand side of the page.
2. List of knots which belong to user and user's followings, also a place for sharing knots in the middle of the page.
3. Existing groups' list and their descriptions on the right hand side of the page.

.. figure:: /images/home_page.png
    :alt: home page
    :width: 800px
    :height: 400px
    :align: center

    The home page of Knitter

In the home page, user can share his/her idea writing it to little textbox and clicking "Knot" button on top of the page.
Besides that, user can edit or delete only her/his own knots from the "..." button on the top-right corner of the knot component.
There are not any "..." button in the knots which belong to user's followings for deleting or editing.

.. figure:: /images/home_page_delete-update_buttons.png
    :alt: home page
    :width: 400px
    :height: 200px
    :align: center

    Delete and update buttons of a knot

    If the user clicks the "Delete This Knot" button, selected knot is removed.
    If the user clicks the "Update This Knot" button, a modal is opened and user can enter new content of the knot and update it.

.. figure:: /images/home_page_update_knot.png
    :alt: home page
    :width: 800px
    :height: 400px
    :align: center

    Update knot content

    In addition to these features, user can also like or reknot a knot and like number or reknot number of the knot increases.
    If user clicks already clicked like or reknot button of same knot, like number or reknot number decreases.

Books Page
----------

Books page consists of shelves for storing user's books, user's recorded books and quotes which are taken from user's registered books by user.

.. figure:: /images/books_page.png
    :alt: books page
    :width: 800px
    :height: 400px
    :align: center

    The books page of Knitter

User should create a shelf for adding books. It is the same logic with a library, books are located in shelves.
User can choose which shelf will be displayed as first shelf in bookcase.
When user click the "+" button on left side of the page, a modal is opened to enter shelf information.

.. figure:: /images/books_page_add_shelf.png
    :alt: books page
    :width: 400px
    :height: 200px
    :align: center

    Add shelf to bookcase

User can also edit and delete shelf's information from buttons next to the shelf name. User enters the shelf information to this window:

.. figure:: /images/books_page_edit_shelf.png
    :alt: books page
    :width: 800px
    :height: 400px
    :align: center

    Update shelf information

Additionally, user adds books to selected shelf from "+" button next to the shelf name. User enters the book information to this window:

.. figure:: /images/books_page_add_book.png
    :alt: books page
    :width: 800px
    :height: 400px
    :align: center

    Add book to selected shelf

User can edit or delete selected book from buttons below the book name.

.. figure:: /images/books_page_update_book.png
    :alt: books page
    :width: 800px
    :height: 400px
    :align: center

    Update book information

Also user's review about book can be seen from folder button in the bottom of the book's component.

.. figure:: /images/books_page_review.png
    :alt: books page
    :width: 800px
    :height: 400px
    :align: center

    User's review about selected book

User can add quotes from recorded books from "+" button next to "Quotes" heading, but first there should be at least one book in user's bookcase.

.. figure:: /images/books_page_add_quote.png
    :alt: books page
    :width: 800px
    :height: 400px
    :align: center

    Add quote from a specific book

User can delete or update added quote from the buttons next to book name below the quotes tab.

.. figure:: /images/books_page_update_quote.png
    :alt: books page
    :width: 800px
    :height: 400px
    :align: center

    Update quote information

