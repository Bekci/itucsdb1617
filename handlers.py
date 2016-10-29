from flask import Blueprint, render_template, redirect, url_for
from components.trends import Trend
from components.trends import Notification
from database import database

site = Blueprint('site', __name__)

@site.route('/')
def login_page():
    return render_template('login_page.html', signedin=False)

@site.route('/home')
def home_page():
    return render_template('home_page.html', signedin=True)

@site.route('/notifications')
def notifications_page():
    trends = [Trend('kismetse-olur','20.000 Knots'),Trend('ben-bilmem-esim-bilir-evi','100.000 Knots'),Trend('survivor-gonulluler','40.000 Knots')]
    notifications = [Notification('https://pbs.twimg.com/profile_images/468699268182999040/o10jbsgO_bigger.jpeg','Ozan ATA','itsozata','Bitsin artik bu cile'),Notification('https://pbs.twimg.com/media/Cu-b95cWEAIQ1V5.jpg','Hakan altun', 'saykolover','Gul Belalidir!'),Notification('https://pbs.twimg.com/profile_images/3354552894/515c6500aabb628256f4dfe03a1e1909_bigger.jpeg','Random Twitter Lady','random','@Ozan is a great guy!')]
    people = ['ozan','was','here']
    return render_template('notifications.html', signedin=True,trends=trends,notifications=notifications,people=people)


@site.route('/user_profile/knots')
def user_profile_page():
    return render_template('user_knots.html',signedin=True)


@site.route('/help')
def help_page():
    return render_template('help_page.html',signedin=True)


@site.route('/settings')
def settings_page():
    return render_template('settings_page.html',signedin=True)


@site.route('/user_profile/followers')
def followers_page():
    return render_template('user_followers.html',signedin=True)


@site.route('/user_profile/following')
def following_page():
    return render_template('user_followings.html',signedin=True)


@site.route('/user_profile/knots')
def knots_page():
    return render_template('user_knots.html',signedin=True)


@site.route('/user_profile/likes')
def likes_page():
    return render_template('user_likes.html',signedin=True)

@site.route('/about_us')
def about_us_page():
    return render_template('about_us.html',signedin=True)


@site.route('/account/change/password')
def change_password_page():
    return render_template('password_change.html', signedin=True)


@site.route('/account/delete/confirm')
def confirm_delete_account_page():
    return render_template('account_delete_confirm.html', signedin=True)

@site.route('/initdb')
def database_initialization():
    database.create_tables()
    database.add_user()
    database.add_knot()
    database.add_relation()
    return redirect(url_for('site.login_page'))
