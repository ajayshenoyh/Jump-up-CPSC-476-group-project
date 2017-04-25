from flask import Flask, render_template, redirect, url_for, make_response
from flask import flash
from wtforms import Form, TextField, validators, PasswordField, BooleanField
#from passlib.hash import sha256_crypt
#from psycopg2.extensions import adapt as thwart
from datetime import datetime
from flask import request
from flask import current_app
from flask_bootstrap import Bootstrap
from HopUp_Database_Code import *
#from JumpUp import JumpUpDB_URL
import os
import urlparse
import smtplib
import psycopg2
import base64

from email.mime.text import MIMEText


msg = MIMEText(
    'From: HopUp \n Subject: Project collaboration invitation \n Hello!! Your team mate is inviting you to collaborate and help with their project on hopup',
    'plain', 'utf-8')
from_addr = 'craftingideas.25@gmail.com'
password = 'SuperUser'
s = smtplib.SMTP_SSL('smtp.gmail.com')
s.login(from_addr, password)

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'

#UploadFolder = '/static/'

ctx = app.app_context()
# flask.g.projectTitl=''
# ctx.push()
bootstrap = Bootstrap(app)
try:
    create_user_table()
    create_project_table()
    create_reward_table()
    create_personal_info_table()
    create_bank_account_info_table()
    create_project_detailed_info_table()
except:
    pass

@app.route('/')
def test():
    return render_template("home.html")


@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/app_name')
def app_context_learning():
    print(app.url_map)
    return current_app.name


@app.route('/login')
def login():
    return render_template("login.html")



#@app.route('/loginback', methods=['POST', 'GET'])
#def loginback():
#    uname = request.form.get('uname')
#    return "Hello %s" % (uname)


class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice',
                              [validators.Required()])

@app.route('/register/', methods=["GET", "POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username = str(form.username.data)
            email = str(form.email.data)
            #password = sha256_crypt.encrypt((str(form.password.data)))
            password=str(form.password.data)
            c, conn = connection()

            c.execute("Select EXISTS (SELECT * FROM USERS WHERE username = %s)",(username,))
            if c.fetchone():
                flash('That username is already taken, please choose another')
                return render_template('register.html', form=form)

            else:
                c.execute("INSERT INTO USERS(UserName, PassWord, EmailId) VALUES (%s, %s, %s)",(username,password,email))
                conn.commit()
                flash('Thanks for registering!')
                #gc.collect()

                #session['logged_in'] = True
                #session['username'] = username

                return redirect(url_for('explore'))

        return render_template("register.html", form=form)

    except Exception as e:
        return (str(e))


@app.route('/story', methods=['POST', 'GET'])
def story():
    if request.method == 'GET':
        return render_template("story.html")
    elif request.method == 'POST':
        pt = request.cookies.get('projectTitle')
        project_video_link = request.form.get('projectVideoLink')
        project_Detailed_Description = request.form.get('projectDetails')
        pdid = len(view_project_detailed_info()) + 1
        add_project_detailed_info(pdid, pt, project_video_link, project_Detailed_Description)
        return render_template('more_about_you.html')


@app.route('/project_register', methods=['POST', 'GET'])
def project_registration():
    if request.method == 'GET':
        resp = make_response(render_template('register_project.html'))
        resp.set_cookie('UserName', '')
        return resp
    elif request.method == 'POST':
        project_title = request.form.get('project_title')
        project_category = request.form.get('ddl1')
        project_sub_category = request.form.get('ddl2')
        project_country = request.form.get('projectCountry')
        project_image = request.form.get('project_image')
        project_description = request.form.get('project_description')
        project_location = request.form.get('project_location')
        project_fund_duration = request.form.get('fund_duration')
        project_fund_goal = request.form.get('fundGoal')
        dt = str(datetime.now())
        # print(type(project_image))
        # image_str = base64.b64encode(request.files.get('project_image',''))
        projects = search_projects_by_title(project_title)
        if len(projects) >= 1:
            return render_template("register_project.html")
        else:
            next_id = len(view_projects()) + 1
            un = request.cookies.get('UserName')
            add_project(next_id, project_title, un, project_category, project_sub_category, project_country,
                        project_image, project_description, project_location, project_fund_duration, project_fund_goal,project_fund_goal,dt)
        resp = make_response(render_template('rewards.html'))
        resp.set_cookie('projectTitle', project_title)
        reward()
        return resp


@app.route('/invite', methods=['POST', 'GET'])
def invite():
    return render_template("invite_collaborator.html")


@app.route('/more_about_you', methods=['POST', 'GET'])
def more_about_you():
    if request.method == 'GET':
        return render_template("more_about_you.html")
    elif request.method == 'POST':
        profile_image = request.form.get('profileimage')
        facebook_url = request.form.get('fbProfile')
        personal_website_url = request.form.get('website')
        personal_location = request.form.get('location')
        github_url = request.form.get('giturl')
        biography = request.form.get('biography')
        next_id = len(view_personal_info()) + 1
        un = request.cookies.get('UserName')
        add_personal_info(next_id, un, profile_image, facebook_url, personal_website_url, personal_location, github_url,
                          biography)
        return render_template('bank_details.html')


@app.route('/account_details', methods=['POST', 'GET'])
def account_details():
    if request.method == 'GET':
        return render_template("bank_details.html")
    elif request.method == 'POST':
        contact_email = request.form.get('contactEmail')
        firstName = request.form.get('fn')
        lastName = request.form.get('ln')
        DOB = request.form.get('DOB')
        HomeAddress = request.form.get('homeAddress')
        RoutingNumber = request.form.get('routingNumber')
        bankAccountNumber = request.form.get('BankAccountNumber')
        next_id = len(view_bank_account_info()) + 1
        un = request.cookies.get('UserName')
        add_bank_account_info(next_id, un, contact_email, firstName, lastName, DOB, HomeAddress, RoutingNumber,
                              bankAccountNumber)
        #project_details = search_projects_by_title(request.cookies.get('projectTitle'))
        project_details = view_projects()
        return render_template('project_overview.html', projectList=project_details)


@app.route('/send_invite', methods=['POST', 'GET'])
def send_invite():
    to_addr = request.form.get('col_email')
    s.sendmail(from_addr, [to_addr], msg.as_string())
    return "Successfully sent invitation"

@app.route('/explore',methods=['POST','GET'])
def explore():
    projects = view_projects()
    return render_template('project_overview.html',projectList=projects)


@app.route('/save_reward', methods=['POST', 'GET'])
def save_reward():
    ## Database code to save the rewad details in the reward table
    return redirect(url_for('reward'))


@app.route('/reward', methods=['POST', 'GET'])
def reward():
    if request.method == 'GET':
        print(request.cookies.get('projectTitle'))
        return render_template("rewards.html")
    elif request.method == 'POST':
        reward_title = request.form.get('rewardTitle')
        pledged_amount = request.form.get('pledgedAmount')
        reward_description = request.form.get('rewardDescription')
        expected_delivery_month = request.form.get('month')
        expected_delivery_year = request.form.get('year')
        shippingDetails = request.form.get('shippingDetails')
        reward_limit = request.form.get('rewardLimit')
        un = request.cookies.get('UserName')
        pt = request.cookies.get('projectTitle')
        next_id = len(view_rewards()) + 1
        add_reward(next_id, reward_title, pt, un, pledged_amount, reward_description, expected_delivery_month,
                   expected_delivery_year, shippingDetails, reward_limit)
        return render_template('more_about_you.html')

@app.route('/donate',methods=['POST','GET'])
def donate():
    if request.method == 'GET':

        return render_template('donateAmount.html')
    elif request.method == 'POST':
        id = request.form.get('projectID')
        fn = request.form.get('fn')
        ln = request.form.get('ln')
        rem = request.form.get('rem')
        rem_amount = int(rem) - int(amount_pledged)
        amount_pledged = request.form.get('pledgeAmount')
        address = request.form.get('address')
        mobileNumber = request.form.get('mobileNumber')
        project_pledged_amount(amount_pledged,str(rem_amount))
        return "Pledged Successfully"

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


def validate_project_title(ptitle):
    if not ptitle.isalpha():
        return False
    else:
        return True


def validate_funding_duration(pfunddur):
    if not pfunddur.isdigit():
        return False
    else:
        return True


def validate_fund_goal(pfundgoal):
    if not pfundgoal.isdigit():
        return False
    else:
        return True


if __name__ == "__main__":
    app.run(debug=True)
