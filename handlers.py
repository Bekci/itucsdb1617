from flask import Blueprint, render_template, redirect, url_for, request
from components.trends import Trend
from database import database
from knot import KnotDatabaseOPS
from user import UserDatabaseOPS, User
from notification import NotificationDatabaseOPS
from poll import PollDatabaseOPS
from interaction import InteractionDatabaseOPS
from message import MessageDatabaseOPS
from shelf import ShelfDatabaseOPS
from book import BookDatabaseOPS
from datetime import datetime
from city import CityDatabaseOPS, City
from events import EventDatabaseOPS
from group import GroupDatabaseOPS
from currency import CurrencyDatabaseOPS, Currency
from sales import  SaleDatabaseOPS, Sale
from quote import QuoteDatabaseOPS
from flask import abort
import urllib
from flask_login import login_user, login_required, logout_user, current_user

site = Blueprint('site', __name__)

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
                    return redirect(url_for('site.user_profile_page', user_id=user.id))

        return render_template('login_page.html', error=True, signedin=False)


@site.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'GET':
        all_cities = CityDatabaseOPS.select_all_cities()
        return render_template('signup_page.html', signedin=False, cities=all_cities)
    else:
        if 'signup' in request.form:
            user = UserDatabaseOPS.select_user(request.form['knittername'])

            samename = False

            if user and user != -1:
                if user.username == request.form['knittername']:
                    return render_template('signup_page.html', samename=True)
            else:
                UserDatabaseOPS.add_user(request.form['knittername'], request.form['inputPassword'],
                                         request.form['profile_pic'], request.form['cover_pic'],
                                         request.form['inputEmail'])

                selected_city_id = request.form['city_id']

                UserDatabaseOPS.add_user_detail(request.form['knittername'], request.form['real_name'],
                                                request.form['real_surname'], selected_city_id)

            return render_template('login_page.html', newly_signup=True, signedin=False, samename=samename)


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


@site.route('/home/knots/<int:user_id>', methods=['GET', 'POST'])
@login_required
def home_page_knots(user_id):
    user = UserDatabaseOPS.select_user_with_id(user_id)
    if current_user != user:
        abort(403)
    return render_template('home_page.html', signedin=True, user=user)


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

            SaleDatabaseOPS.add_item(request.form['item_name_form'], request.form['item_picture_form'],
                                     request.form['item_price_form'],
                                     request.form['item_description_form'], request.form['item_change_currency'])

            SaleDatabaseOPS.add_sale(user_id, SaleDatabaseOPS.select_new_item_id(request.form['item_name_form'], request.form['item_picture_form'],
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
                my_item_list = SaleDatabaseOPS.select_sales_of_a_user(request.form['keyword'])
            elif request.form['choose_search'] == 'closest':
                my_item_list = SaleDatabaseOPS.select_closest_items(user.username, my_city.id)
            elif request.form['choose_search'] == 'price':
                my_item_list = SaleDatabaseOPS.select_items_by_price(user.username, request.form['keyword'], request.form['currency_select'])
            elif request.form['choose_search'] == 'currency':
                my_item_list = SaleDatabaseOPS.select_items_by_currency(request.form['currency_select'], user.username)
            elif request.form['choose_search'] == 'place':
                my_item_list = SaleDatabaseOPS.select_items_by_place(request.form['city_select'])
            elif request.form['choose_search'] == 'newest':
                my_item_list = SaleDatabaseOPS.select_newest_items(user.username)


    return render_template('sales_knitter.html', signedin=True, user=user, real_name=real_name,
                               my_city=my_city, cities=cities, currency_list=currency_list, my_item_list=my_item_list,isSearched=_isSearched)


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
        like_list = KnotDatabaseOPS.get_likes(user_id)
        followers = UserDatabaseOPS.get_followers(user_id)
        followings = UserDatabaseOPS.get_following(user_id)
        lengths = {'knot_len': len(knot_list), 'like_len': len(like_list), 'followers_len': len(followers),
                   'followings_len': len(followings)}
        return render_template('user_profile.html', signedin=True, user=user, real_name=real_name,
                               my_city=my_city, cities=cities, knot_list=knot_list, user_check=user_check,
                               likes=like_list, followers=followers, followings=followings, lengths=lengths)
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
                UserDatabaseOPS.add_user_detail(user.username, my_name, my_surname, city_id)
            else:
                UserDatabaseOPS.update_user_detail(user.username, my_name, my_surname, city_id)

            UserDatabaseOPS.update_user(user.username, user.password,
                                        user.profile_pic, user.cover_pic, user.mail_address)

            real_name = UserDatabaseOPS.select_user_detail(user.username)
            my_city = CityDatabaseOPS.select_city(real_name.city, real_name.country)
            knot_list = KnotDatabaseOPS.select_knots_for_owner(user.id)
            like_list = KnotDatabaseOPS.get_likes(user_id)
            followers = UserDatabaseOPS.get_followers(user_id)
            followings = UserDatabaseOPS.get_following(user_id)
            lengths = {'knot_len': len(knot_list), 'like_len': len(like_list), 'followers_len': len(followers),
                       'followings_len': len(followings)}

        if 'deleteReal' in request.form:
            user = UserDatabaseOPS.select_user_with_id(user_id)
            UserDatabaseOPS.delete_user_detail(user.username)
            real_name = UserDatabaseOPS.select_user_detail(user.username)
            my_city = CityDatabaseOPS.select_city(real_name.city, real_name.country)
            knot_list = KnotDatabaseOPS.select_knots_for_owner(user.id)
            like_list = KnotDatabaseOPS.get_likes(user_id)
            followers = UserDatabaseOPS.get_followers(user_id)
            followings = UserDatabaseOPS.get_following(user_id)
            lengths = {'knot_len': len(knot_list), 'like_len': len(like_list), 'followers_len': len(followers),
                       'followings_len': len(followings)}

        return render_template('user_profile.html', signedin=True, user=user, real_name=real_name,
                               my_city=my_city, cities=cities, knot_list=knot_list, user_check=user_check,
                               likes=like_list, followers=followers, followings=followings, lengths=lengths)


@site.route('/help')
def help_page():
    return render_template('help_page.html', signedin=True)

@site.route('/settings/<int:user_id>', methods=['GET', 'POST'])
@login_required
def settings_page(user_id):
    user = UserDatabaseOPS.select_user_with_id(user_id)
    if current_user != user:
        abort(403)
    if request.method == 'GET':

        real_name = UserDatabaseOPS.select_user_detail(user.username)
        return render_template('settings_page.html', signedin=True, user=user, real_name=real_name, error=False)
    else:
        if 'change-mail' in request.form:
            mail = request.form['mail_address']
            real_name = UserDatabaseOPS.select_user_detail(user.username)
            UserDatabaseOPS.update_user(user.username, user.password, user.profile_pic, user.cover_pic, mail)
            changed_user = UserDatabaseOPS.select_user_with_id(user_id)
        elif 'add-group' in request.form:
            user = UserDatabaseOPS.select_user_with_id(user_id)
            real_name = UserDatabaseOPS.select_user_detail(user.username)
            group_name = request.form['group_name']
            group_profile_pic = request.form['group_picture_url']
            group_description = request.form['group_description']
            group_id = GroupDatabaseOPS.add_group(group_name, group_profile_pic, group_description)
            GroupDatabaseOPS.add_group_participation(group_id, user_id)
            changed_user = UserDatabaseOPS.select_user_with_id(user_id)

        return render_template('settings_page.html', signedin=True, user=changed_user, real_name=real_name, success=True)



@site.route('/about_us')
def about_us_page():
    return render_template('about_us.html', signedin=True)


@site.route('/account/<int:user_id>/change/password', methods=['GET', 'POST'])
@login_required
def change_password_page(user_id):
    user = UserDatabaseOPS.select_user_with_id(user_id)
    if current_user != user:
        abort(403)
    if request.method == 'GET':
        real_name = UserDatabaseOPS.select_user_detail(user.username)
        return render_template('password_change.html', signedin=True, user=user, real_name=real_name, error=False)
    else:
        current_password = request.form['CurrentPassword']
        new_password = request.form['NewPassword']
        confirm_password = request.form['ConfirmPassword']
        real_name = UserDatabaseOPS.select_user_detail(user.username)
        user = UserDatabaseOPS.select_user_with_id(user_id)
        if current_password != user.password:
            return render_template('password_change.html', signedin=True, user=user, real_name=real_name, password_error=True)
        elif new_password != confirm_password:
             return render_template('password_change.html', signedin=True, user=user, real_name=real_name, password_match_error=True)
        else:
            UserDatabaseOPS.update_user(user.username, new_password, user.profile_pic, user.cover_pic, user.mail_address)
        return render_template('password_change.html', signedin=True, user=user, real_name=real_name, success=True)


@site.route('/account/<int:user_id>/delete/confirm', methods=['GET', 'POST'])
@login_required
def confirm_delete_account_page(user_id):
    user = UserDatabaseOPS.select_user_with_id(user_id)
    if current_user != user:
        abort(403)
    if request.method == 'GET':
        return render_template('account_delete_confirm.html', signedin=True, user=user)
    else:
        UserDatabaseOPS.delete_user(user.username)
        return redirect(url_for('site.login_page'))


@site.route('/initdb')
def database_initialization():
    database.create_tables()
    return redirect(url_for('site.login_page'))


@site.route('/messages/<int:user_id>', methods=['GET', 'POST'])
@login_required
def messages_page(user_id):

    user = UserDatabaseOPS.select_user_with_id(user_id)
    if current_user != user:
        abort(403)
    my_followings = InteractionDatabaseOPS.select_followings_from_user_interaction(user_id)
    my_followers = InteractionDatabaseOPS.select_followers_from_user_interaction(user_id)
    contact_list = []
    for my_following in my_followings:
        if my_following in my_followers:
            contact_list.append(my_following)
    contact_user_list = []
    for contact_id in contact_list:
        contact = UserDatabaseOPS.select_user_with_id(contact_id)
        contact_user_list.append(contact)
    all_messages = []
    for contact in contact_list:
        messages = MessageDatabaseOPS.select_messages_for_chat(user_id, contact)
        all_messages.append(messages)

    if request.method == 'GET':
        messages=MessageDatabaseOPS.select_messages_for_user(user_id)
        return render_template('messages.html', signedin=True, user=user, all_messages=all_messages, contact_user_list=contact_user_list)
    else:

        if 'send_new_message' in request.form:

            content = request.form['message_content']
            to_user_id = request.form['to_user_id']
            MessageDatabaseOPS.add_message(content,user_id, to_user_id)
            return redirect(url_for('site.messages_page', user_id=user_id))
        elif 'response_answer' in request.form:
            content = request.form['message_content']
            to_user_id = request.form['to_user_id']
            MessageDatabaseOPS.add_message(content,user_id, to_user_id)
            return redirect(url_for('site.messages_page', user_id=user_id))
        elif 'delete_messages' in request.form:
            index = int(request.form['chat_id'])
            for message in all_messages[index]:
                MessageDatabaseOPS.delete_message(message.message_id)
            return redirect(url_for('site.messages_page', user_id=user_id))


@site.route('/groups/<int:group_id>/<int:user_id>', methods=['GET', 'POST'])
@login_required
def group_page(group_id, user_id):
    user = UserDatabaseOPS.select_user_with_id(user_id)
    if current_user != user:
        abort(403)
    group_participants = GroupDatabaseOPS.select_group_participation(group_id)
    group_info = GroupDatabaseOPS.select_group(group_id)
    joined=False
    knot_list = []
    group_knots_id = [obj.knot_id for obj in GroupDatabaseOPS.select_group_knot(group_id) ]
    for knot_id in group_knots_id:
        knot = KnotDatabaseOPS.select_knot(knot_id)
        if knot != -1:
            knot_list.append(knot)
    for participant in group_participants:
        if user_id == participant.user_id:
            joined=True
    if request.method=='GET':

        return render_template('groups.html', joined=joined, signedin=True, user=user, group_participants=group_participants, group_info=group_info, group_knots=knot_list)
    elif request.method=='POST':
        if 'update-description' in request.form:
            group_description = request.form['group_description']
            GroupDatabaseOPS.update_group_description(group_id, group_description)
        elif 'delete-group' in request.form:
            GroupDatabaseOPS.delete_group(group_id)
            return redirect(url_for('site.user_profile_page', user_id=user_id))
        elif 'join-group' in request.form:
            group_id = int(request.form["join-group"])
            GroupDatabaseOPS.add_group_participation(group_id,user_id)
        elif 'exit-group' in request.form:
            group_id = int(request.form["exit-group"])
            GroupDatabaseOPS.exit_group_participation(group_id, user_id)
        elif 'add_group_knot' in request.form:
            knot_content = request.form['knot_content']
            group_id = group_id
            knot_id = KnotDatabaseOPS.add_knot(user_id, knot_content, 0, 0, True, datetime.now().date().isoformat())
            GroupDatabaseOPS.add_group_knot(group_id, knot_id)
        return redirect(url_for('site.group_page', group_id=group_id, user_id=user_id))


@site.route('/events/<int:user_id>', methods=['GET', 'POST'])
@login_required
def events_page(user_id):
    user = UserDatabaseOPS.select_user_with_id(user_id)
    if current_user != user:
        abort(403)
    if request.method == 'GET':
        organizer_ids = []
        organizer_ids.append(user_id)
        my_events = EventDatabaseOPS.select_organized_events_with_user_id(user_id)
        joined_events = EventDatabaseOPS.select_joined_events_with_user_id(user_id)
        joinable_events = EventDatabaseOPS.select_joinable_events_with_user_id(user_id)
        return render_template('events.html', signedin=True, user=user, my_events=my_events, joined_events=joined_events, joinable_events=joinable_events, organizer_ids=organizer_ids)
    elif request.method == 'POST':
        if 'create-event' in request.form:
            owner_id = user_id
            event_content = request.form['description']
            event_start_date = request.form['start-date']
            event_end_date = request.form['end-date']
            if int(request.form['is_user']) == 0:
                is_user=True
            else:
                is_user=False
            event_id = EventDatabaseOPS.add_event(owner_id, event_content, event_start_date, event_end_date, is_user)
            EventDatabaseOPS.add_participant(event_id, user_id)
        elif 'update-event' in request.form:
            event_content = request.form['description']
            event_start_date = request.form['start-date']
            event_end_date = request.form['end-date']
            event_id = request.form['update-event']
            EventDatabaseOPS.update_event(event_content, event_start_date, event_end_date, event_id)
        elif 'delete-event' in request.form:
            event_id = request.form['delete-event']
            EventDatabaseOPS.delete_event(event_id)
        elif 'exit-event' in request.form:
            event_id = request.form['exit-event']
            EventDatabaseOPS.delete_participant(event_id, user_id)
        elif 'join-event' in request.form:
            event_id = request.form['join-event']
            EventDatabaseOPS.add_participant(event_id, user_id)
        return redirect(url_for('site.events_page', user_id=user_id))


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

@site.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.login_page'))


@site.context_processor
def utility_processor():

    def get_real_name(user_id):
        user = UserDatabaseOPS.select_user_with_id(user_id)
        real_name = UserDatabaseOPS.select_user_detail(user.username)
        return real_name

    def get_user_info(user_id):
        user = UserDatabaseOPS.select_user_with_id(user_id)
        return user

    return dict(get_real_name=get_real_name, get_user_info=get_user_info)
