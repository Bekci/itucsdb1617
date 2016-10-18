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
    notifications = [Notification('https://pbs.twimg.com/profile_images/468699268182999040/o10jbsgO_bigger.jpeg','Ozan ATA','itsozata','Bitsin artik bu cile'),Notification('https://pbs.twimg.com/media/Cu-b95cWEAIQ1V5.jpg','Hakan altun', 'saykolover','Gul Belalidir!'),Notification('https://pbs.twimg.com/profile_images/3354552894/515c6500aabb628256f4dfe03a1e1909_bigger.jpeg','Random Twitter Lady','random','@Ozan is a great guy!')]
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

@site.route('/user_profile/followers')
def followers_page():
    return render_template('user_followers.html',signedin=True)

@site.route('/user_profile/following')
def following_page():
    return render_template('user_followings.html',signedin=True)

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
    def __init__(self,img, name, username,tweet):
        self.img = img
        self.name = name
        self.username = username
        self.tweet = tweet
