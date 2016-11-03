from flask import Blueprint, render_template, redirect, url_for, request, g
from components.trends import Trend
from components.trends import Notification
from database import database
from knot import KnotDatabaseOPS
from user import UserDatabaseOPS
from notification import NotificationDatabaseOPS
from interaction import InteractionDatabaseOPS

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
                    return redirect(url_for('site.user_profile_page', user_id=user.id))

        return render_template('login_page.html', error=True, signedin=False)


@site.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'GET':
        return render_template('signup_page.html', signedin=False)
    else:
        if 'signup' in request.form:
            user = UserDatabaseOPS.select_user(request.form['knittername'])

            if user and user != -1:
                if user.username == request.form['knittername']:
                    return render_template('signup_page.html', samename=True)
            else:
                UserDatabaseOPS.add_user(request.form['knittername'], request.form['inputPassword'],
                                         request.form['profile_pic'], request.form['cover_pic'],
                                         request.form['inputEmail'])

            return render_template('login_page.html', newly_signup=True, signedin=False)


@site.route('/home/<int:user_id>')
def home_page(user_id):
    user = UserDatabaseOPS.select_user_with_id(user_id)
    return render_template('home_page.html', signedin=True, user=user)


@site.route('/home/knots/<int:user_id>')
def home_page1(user_id):
    user = UserDatabaseOPS.select_user_with_id(user_id)
    return render_template('home_page.html', signedin=True, user=user)

@site.route('/notifications/<int:user_id>', methods = ['GET','POST'])
def notifications_page(user_id):
    user = UserDatabaseOPS.select_user_with_id(user_id)
    trends = [Trend('kismetse-olur','20.000 Knots'),Trend('ben-bilmem-esim-bilir-evi','100.000 Knots'),Trend('survivor-gonulluler','40.000 Knots')]
    knots = NotificationDatabaseOPS.select_notifications(user)
    if request.method == 'GET':
        return render_template('notifications.html', signedin=True,trends=trends,knots=knots, user = user)

    else:
        if 'delete' in request.form:
            knot_id = request.form['delete']
            UserDatabaseOPS.delete_knot(knot_id)
        elif 'update' in request.form:
            knot_id = request.form['update']
            print("Update Knot function is currently not working :(")
        elif 'like' in request.form:
            knot_id = request.form['like']
            is_like = NotificationDatabaseOPS.check_like(knot_id,user, True)
            if is_like:
                NotificationDatabaseOPS.delete_relation(knot_id, user, True)
                NotificationDatabaseOPS.decrease_knot_like(knot_id)
            else:
                NotificationDatabaseOPS.insert_relation(knot_id, user, True)
                NotificationDatabaseOPS.increase_knot_like(knot_id)
        elif 'reknot' in request.form:
            knot_id = request.form['reknot']
            is_reknot = NotificationDatabaseOPS.check_reknot(knot_id,user, False)
            if is_reknot:
                NotificationDatabaseOPS.delete_relation(knot_id, user, False)
                NotificationDatabaseOPS.decrease_knot_reknot(knot_id)
            else:
                NotificationDatabaseOPS.insert_relation(knot_id, user, False)
                NotificationDatabaseOPS.increase_knot_reknot(knot_id)

        knots = NotificationDatabaseOPS.select_notifications(user)
        return render_template('notifications.html', signedin=True,trends=trends,knots=knots, user = user)


@site.route('/user_profile/<int:user_id>', methods=['GET', 'POST'])
def user_profile_page(user_id):

    if request.method == 'GET':
        user = UserDatabaseOPS.select_user_with_id(user_id)
        real_name = UserDatabaseOPS.select_user_name_surname(user.username)
        return render_template('user_profile.html', signedin=True, user=user, real_name=real_name)
    else:
        if 'changeImage' in request.form:
            user = UserDatabaseOPS.select_user_with_id(user_id)
            user.profile_pic = request.form['imageURL']
            my_name = request.form['my_name']
            my_surname = request.form['my_surname']
            user.cover_pic = request.form['coverURL']

            user_real_name = UserDatabaseOPS.select_user_name_surname(user.username)

            if user_real_name == -1:
                UserDatabaseOPS.add_real_name(user.username,my_name, my_surname)
            else:
                UserDatabaseOPS.update_real_name(user.username, my_name, my_surname)

            UserDatabaseOPS.update_user(user.username, user.password,
                                        user.profile_pic, user.cover_pic, user.mail_address)

            user_real_name = UserDatabaseOPS.select_user_name_surname(user.username)

        return render_template('user_profile.html', signedin=True, user=user, real_name=user_real_name)


@site.route('/help')
def help_page():
    return render_template('help_page.html', signedin=True)


@site.route('/settings/<int:user_id>', methods=['GET', 'POST'])
def settings_page(user_id):
    if request.method == 'GET':
        user = UserDatabaseOPS.select_user_with_id(user_id)
        real_name = UserDatabaseOPS.select_user_name_surname(user.username)
        return render_template('settings_page.html', signedin=True, user=user, real_name=real_name, error=False)
    else:
        mail = request.form['mail_address']
        user = UserDatabaseOPS.select_user_with_id(user_id)
        real_name = UserDatabaseOPS.select_user_name_surname(user.username)
        UserDatabaseOPS.update_user(user.username, user.password, user.profile_pic, user.cover_pic, mail)
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
        real_name = UserDatabaseOPS.select_user_name_surname(user.username)
        return render_template('password_change.html', signedin=True, user=user, real_name=real_name, error=False)
    else:
        current_password = request.form['CurrentPassword']
        new_password = request.form['NewPassword']
        confirm_password = request.form['ConfirmPassword']
        user = UserDatabaseOPS.select_user_with_id(user_id)
        real_name = UserDatabaseOPS.select_user_name_surname(user.username)
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
    UserDatabaseOPS.add_user("mesut_guneri", "tokmak", "tokmak", "tokmak",
                             "cobanyildizi")  # Can Altinigne Insert Into User Table Manually
    KnotDatabaseOPS.add_knot(1, "First content of the Knitter", 0, 0, "2016-10-29")
    InteractionDatabaseOPS.add_user_interaction(1, 10)  # ilknur meray: insert into USER_INTERACTION table manually
    database.add_relation()
    database.add_message()
    return redirect(url_for('site.login_page'))


@site.route('/messages/<int:user_id>')
def messages_page(user_id):
    user = UserDatabaseOPS.select_user_with_id(user_id)
    return render_template('messages.html', signedin=True, user=user)
