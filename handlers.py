from flask import Flask, Blueprint, render_template
from flask import current_app

from datetime import datetime

site = Blueprint('site', __name__)

@site.route('/')
def login_page():
    return render_template('login_page.html', signedin=False)

@site.route('/home')
def home_page():
    return render_template('home_page.html', signedin=True,username="Ozan ATA")

@site.route('/notifications')
def notifications_page():
    trends = [Trend('ozan','20.000 tweets'),Trend('berlin','100.000 tweets'),Trend('merinos','40.000 tweets')]
    notifications = [Notification('Ozan','Bitsin artik bu cile'),Notification('Hakan altun','Gul Belalidir!'),Notification('Random Twitter Lady','@Ozan is a great guy!')]
    people = ['ozan','was','here']
    return render_template('notifications.html', signedin=True,trends=trends,notifications=notifications,people=people)

@site.route('/user_profile')
def user_profile_page():
    return render_template('user_profile.html',signedin=True)


@site.route('/help')
def help_page():
    return render_template('help_page.html',signedin=True)

@site.route('/settings')
def settings_page():
    return render_template('settings_page.html',signedin=True)

@site.route('/user_profile/user_followers')
def followers_page():
    return render_template('user_followers.html',signedin=True)

@site.route('/about_us')
def about_us_page():
    return render_template('about_us.html',signedin=True)

@site.route('/account/change/password')
def change_password_page():
    return render_template('password_change.html', signedin=True)

@site.route('/account/delete/confirm')
def confirm_delete_account_page():
    return render_template('account_delete_confirm.html', signedin=True)


class Trend:
    def __init__(self, name,info):
        self.name = name
        self.info = info

class Notification:
    def __init__(self, source,tweet):
        self.source = source
        self.tweet = tweet
