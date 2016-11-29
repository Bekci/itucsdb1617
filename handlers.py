from flask import Blueprint, render_template, redirect, url_for, request
from components.trends import Trend
from database import database
from knot import KnotDatabaseOPS
from user import UserDatabaseOPS, User
from notification import NotificationDatabaseOPS
from poll import PollDatabaseOPS
from interaction import InteractionDatabaseOPS
from message import MessageDatabaseOPS
from book_type import BookTypeDatabaseOPS
from book import BookDatabaseOPS
from datetime import datetime
from city import CityDatabaseOPS, City
from events import EventDatabaseOPS
from group import GroupDatabaseOPS
from currency import CurrencyDatabaseOPS, Currency
from sales import  SaleDatabaseOPS, Sale

site = Blueprint('site', __name__)

sil_bunu = User(1,'Can', 'can', 'asdasd', 'asdasd', 'asdas', 'asdsad')


@site.route('/', methods=['GET', 'POST'])
def login_page():

    if request.method == 'GET':
        return render_template('login_page.html', signedin=False)
    else:
        if 'Login' in request.form:
            user = UserDatabaseOPS.select_user(request.form['knittername'])

            if user and user != -1:
                if request.form['knotword'] == user.password:
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
def home_page(user_id):
    user = UserDatabaseOPS.select_user_with_id(user_id)
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
            KnotDatabaseOPS.add_knot(user_id, request.form['new_knot_content'], 0, 0, datetime.now().date().isoformat())
            return redirect(url_for('site.home_page', user_id=user.id))
        elif 'delete' in request.form:
            KnotDatabaseOPS.delete_knot(request.form['delete'])
            return redirect(url_for('site.home_page', user_id=user.id))
        elif 'update_knot' in request.form:
            KnotDatabaseOPS.update_knot(user.id, request.form['update_knot_content'], 0, 0, datetime.now().date().isoformat(), request.form['update_knot'])
            return redirect(url_for('site.home_page', user_id=user.id))


@site.route('/books_page/<int:user_id>', methods=['GET', 'POST'])
def books_page(user_id):
    user = UserDatabaseOPS.select_user_with_id(user_id)
    real_name = UserDatabaseOPS.select_user_detail(user.username)
    if request.method == 'GET':
        my_books = BookDatabaseOPS.select_all_books(user.id)
        return render_template('books_page.html', signedin=True, user=user, real_name=real_name, my_books=my_books)
    else:
        if 'add_book' in request.form:
            BookDatabaseOPS.add_book(request.form['title'], request.form['cover'], request.form['writer'], request.form['date_read'], request.form['review'], request.form['b_type_name'], user.id)
            return redirect(url_for('site.books_page', user_id=user.id))
        elif 'add_type' in request.form:
            BookTypeDatabaseOPS.add_book_type(request.form['type_name'])
            return redirect(url_for('site.books_page', user_id=user.id))
        elif 'delete' in request.form:
            BookDatabaseOPS.delete_book(request.form['delete'], user.id)
            return redirect(url_for('site.books_page', user_id=user.id))
        elif 'update_book' in request.form:
    # BookDatabaseOPS.update_book(request.form['new_book_title'], request.form['new_book_cover'], request.form['new_book_writer'], request.form['new_date_read'], request.form['new_book_review'], request.form['new_book_type_name'], user.id)
            return redirect(url_for('site.books_page', user_id=user.id))


@site.route('/home/knots/<int:user_id>', methods=['GET', 'POST'])
def home_page_knots(user_id):
    user = UserDatabaseOPS.select_user_with_id(user_id)
    return render_template('home_page.html', signedin=True, user=user)


@site.route('/notifications/<int:user_id>', methods = ['GET','POST'])
def notifications_page(user_id):
    user = UserDatabaseOPS.select_user_with_id(user_id)
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
def sales_page(user_id):
    if request.method == 'GET':
        user = UserDatabaseOPS.select_user_with_id(user_id)
        real_name = UserDatabaseOPS.select_user_detail(user.username)
        currency_list = CurrencyDatabaseOPS.select_all_currencies()
        my_city = CityDatabaseOPS.select_city(real_name.city, real_name.country)
        cities = CityDatabaseOPS.select_all_cities()
        my_item_list = SaleDatabaseOPS.select_sales_of_a_user(user.username)

        return render_template('sales_knitter.html', signedin=True, user=user, real_name=real_name,
                               my_city=my_city, cities=cities, currency_list=currency_list, my_item_list=my_item_list)


@site.route('/user_profile/<int:user_id>', methods=['GET', 'POST'])
def user_profile_page(user_id):

    if request.method == 'GET':
        user = UserDatabaseOPS.select_user_with_id(user_id)
        real_name = UserDatabaseOPS.select_user_detail(user.username)
        my_city = CityDatabaseOPS.select_city(real_name.city, real_name.country)
        cities = CityDatabaseOPS.select_all_cities()
        knot_list = KnotDatabaseOPS.select_knots_for_owner(user.id)
        return render_template('user_profile.html', signedin=True, user=user, real_name=real_name,
                               my_city=my_city, cities=cities, knot_list=knot_list)
    else:
        if 'changeImage' in request.form:
            user = UserDatabaseOPS.select_user_with_id(user_id)
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

        if 'deleteReal' in request.form:
            user = UserDatabaseOPS.select_user_with_id(user_id)
            UserDatabaseOPS.delete_user_detail(user.username)
            real_name = UserDatabaseOPS.select_user_detail(user.username)
            my_city = CityDatabaseOPS.select_city(real_name.city, real_name.country)
            knot_list = KnotDatabaseOPS.select_knots_for_owner(user.id)

        return render_template('user_profile.html', signedin=True, user=user, real_name=real_name,
                               my_city=my_city, cities=cities, knot_list=knot_list)


@site.route('/help')
def help_page():
    return render_template('help_page.html', signedin=True)

@site.route('/settings/<int:user_id>', methods=['GET', 'POST'])
def settings_page(user_id):
    if request.method == 'GET':
        user = UserDatabaseOPS.select_user_with_id(user_id)
        real_name = UserDatabaseOPS.select_user_detail(user.username)
        return render_template('settings_page.html', signedin=True, user=user, real_name=real_name, error=False)
    else:
        if 'change-mail' in request.form:
            mail = request.form['mail_address']
            user = UserDatabaseOPS.select_user_with_id(user_id)
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
    user = UserDatabaseOPS.select_user_with_id(1)
    return render_template('about_us.html', signedin=True, user=user)


@site.route('/account/<int:user_id>/change/password', methods=['GET', 'POST'])
def change_password_page(user_id):
    if request.method == 'GET':
        user = UserDatabaseOPS.select_user_with_id(user_id)
        real_name = UserDatabaseOPS.select_user_detail(user.username)
        return render_template('password_change.html', signedin=True, user=user, real_name=real_name, error=False)
    else:
        current_password = request.form['CurrentPassword']
        new_password = request.form['NewPassword']
        confirm_password = request.form['ConfirmPassword']
        user = UserDatabaseOPS.select_user_with_id(user_id)
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
def confirm_delete_account_page(user_id):
    if request.method == 'GET':
        user = UserDatabaseOPS.select_user_with_id(user_id)
        return render_template('account_delete_confirm.html', signedin=True, user=user)
    else:
        user = UserDatabaseOPS.select_user_with_id(user_id)
        UserDatabaseOPS.delete_user(user.username)
        return redirect(url_for('site.login_page'))


@site.route('/initdb')
def database_initialization():
    database.create_tables()
    return redirect(url_for('site.login_page'))


@site.route('/messages/<int:user_id>', methods=['GET', 'POST'])
def messages_page(user_id):

    user = UserDatabaseOPS.select_user_with_id(user_id)
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
def group_page(group_id, user_id):
    user = UserDatabaseOPS.select_user_with_id(user_id)
    group_participants = GroupDatabaseOPS.select_group_participation(group_id)
    group_info = GroupDatabaseOPS.select_group(group_id)
    joined=False
    for participant in group_participants:
        if user_id == participant.user_id:
            joined=True
    if request.method=='GET':

        return render_template('groups.html', joined=joined, signedin=True, user=user, group_participants=group_participants, group_info=group_info)
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
        return redirect(url_for('site.group_page', group_id=group_id, user_id=user_id))


@site.route('/events/<int:user_id>', methods=['GET', 'POST'])
def events_page(user_id):
    user = UserDatabaseOPS.select_user_with_id(user_id)
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
