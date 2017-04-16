from flask import Flask, render_template,redirect,url_for,make_response
from flask import flash
from flask import request
from flask import current_app
from flask_bootstrap import Bootstrap
from HopUp_Database_Code import *
import smtplib
import psycopg2
import base64

from email.mime.text import MIMEText
#msg = MIMEText('From: HopUp \n Subject: Project collaboration invitation \n Hello!! Your team mate is inviting you to collaborate and help with their project on hopup','plain','utf-8')
#from_addr = 'srushti.gangireddy@gmail.com'
#password='SRIRAMA1!'
#to_addr = 'srushti.gangireddy@gmail.com'
#s =smtplib.SMTP_SSL('smtp.gmail.com')
#s.login(from_addr,password)

app=Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'

UploadFoler = '/static/'

ctx = app.app_context()
#flask.g.projectTitl=''
#ctx.push()
bootstrap=Bootstrap(app)



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

@app.route('/loginback',methods=['POST','GET'])
def loginback():
    uname = request.form.get('uname')
    return "Hello %s" %(uname)

@app.route('/story',methods=['POST','GET'])
def story():
    if request.method == 'GET':
        return render_template("story.html")
    elif request.method == 'POST':
        print(request.cookies.get('projectTitle'))
        project_video_link = request.form.get('projectVideoLink')
        project_Detailed_Description = request.form.get('projectDetails')
        return render_template('more_about_you.html')

@app.route('/project_register',methods=['POST','GET'])
def project_registration():
    if request.method == 'GET':
        return render_template("register_project.html")
    elif request.method == 'POST':
        project_title = request.form.get('project_title')
        project_category = request.form.get('ddl1')
        project_sub_category = request.form.get('ddl2')
        project_country = request.form.get('projectCountry')
        #project_image = request.files.get('project_image','')
        project_description = request.form.get('project_description')
        project_location = request.form.get('project_location')
        project_fund_duration = request.form.get('fund_duration')
        project_fund_goal = request.form.get('fundGoal')
        #print(type(project_image))
        #image_str = base64.b64encode(request.files.get('project_image',''))
        if 'file' not in request.files:
            flash("No file upload")
        file = request.files['project_image']
        print(type(file))
        file.save(os.path.join)
        resp = make_response(render_template('rewards.html'))
        resp.set_cookie('projectTitle',project_title)
        reward()
        return resp

@app.route('/invite',methods=['POST','GET'])
def invite():
    return render_template("invite_collaborator.html")

@app.route('/more_about_you',methods=['POST','GET'])
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
        return render_template('bank_details.html')

@app.route('/account_details',methods=['POST','GET'])
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
        return render_template('home.html')

@app.route('/send_invite',methods=['POST','GET'])
def send_invite():
    #to_addr = request.form.get('col_email')
    #s.sendmail(from_addr,[to_addr],msg.as_string())
    return "Successfully sent invitation"

@app.route('/save_reward',methods=['POST','GET'])
def save_reward():
    ## Database code to save the rewad details in the reward table
    return redirect(url_for('reward'))

@app.route('/reward',methods=['POST','GET'])
def reward():
    if request.method == 'GET':
        print(request.cookies.get('projectTitle'))
        return render_template("rewards.html")
    elif request.method == 'POST':
        reward_title = request.form.get('rewardTitle')
        pledged_amount = request.form.get('rewardTitle')
        reward_description = request.form.get('rewardDescription')
        expected_delivery_month = request.form.get('month')
        expected_delivery_year = request.form.get('year')
        shippingDetails = request.form.get('shippingDetails')
        reward_limit = request.form.get('rewardLimit')
        return render_template('more_about_you.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

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

if __name__=="__main__":
    app.run(debug=True)
