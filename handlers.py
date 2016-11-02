from flask import Blueprint, render_template, redirect, url_for, request
from components.trends import Trend
from components.trends import Notification
from database import database
from knot import KnotDatabaseOPS
from user import UserDatabaseOPS
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
                    return render_template('user_knots.html', user=user, signedin=True)

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

        return render_template('login_page.html', signedin=False, newly_signup=True)


@site.route('/home')
def home_page():
    return render_template('home_page.html', signedin=True)


@site.route('/home/knots')
def home_page1():
    return render_template('home_page.html', signedin=True)


@site.route('/notifications')
def notifications_page():
    trends = [Trend('kismetse-olur', '20.000 Knots'), Trend('ben-bilmem-esim-bilir-evi', '100.000 Knots'),
              Trend('survivor-gonulluler', '40.000 Knots')]
    notifications = [
        Notification('https://pbs.twimg.com/profile_images/468699268182999040/o10jbsgO_bigger.jpeg', 'Ozan ATA',
                     'itsozata', 'Bitsin artik bu cile'),
        Notification('https://pbs.twimg.com/media/Cu-b95cWEAIQ1V5.jpg', 'Hakan altun', 'saykolover', 'Gul Belalidir!'),
        Notification('https://pbs.twimg.com/profile_images/3354552894/515c6500aabb628256f4dfe03a1e1909_bigger.jpeg',
                     'Random Twitter Lady', 'random', '@Ozan is a great guy!')]
    people = ['ozan', 'was', 'here']
    return render_template('notifications.html', signedin=True, trends=trends, notifications=notifications,
                           people=people)


@site.route('/user_profile/knots')
def user_profile_page():
    return render_template('user_knots.html', signedin=True)


@site.route('/help')
def help_page():
    return render_template('help_page.html', signedin=True)


@site.route('/settings')
def settings_page():
    return render_template('settings_page.html', signedin=True)


@site.route('/user_profile/followers')
def followers_page():
    return render_template('user_followers.html', signedin=True)


@site.route('/user_profile/following')
def following_page():
    return render_template('user_followings.html', signedin=True)


@site.route('/user_profile/knots')
def knots_page():
    return render_template('user_knots.html', signedin=True)


@site.route('/user_profile/likes')
def likes_page():
    return render_template('user_likes.html', signedin=True)


@site.route('/about_us')
def about_us_page():
    return render_template('about_us.html', signedin=True)


@site.route('/account/change/password')
def change_password_page():
    return render_template('password_change.html', signedin=True)


@site.route('/account/delete/confirm')
def confirm_delete_account_page():
    return render_template('account_delete_confirm.html', signedin=True)


@site.route('/initdb')
def database_initialization():
    database.create_tables()
    UserDatabaseOPS.add_user("mesut_guneri", "tokmak", "tokmak", "tokmak",
                             "cobanyildizi")  # Can Altinigne Insert Into User Table Manually
    KnotDatabaseOPS.add_knot(1, "First content of the Knitter", 0, 0, "2016-10-29")
    InteractionDatabaseOPS.add_user_interaction(1, 10)  # ilknur meray: insert into USER_INTERACTION table manually
    database.add_relation()
    database.add_user_interaction()
    database.add_message()
    return redirect(url_for('site.login_page'))


@site.route('/messages')
def messages_page():
    return render_template('messages.html', signedin=True)
