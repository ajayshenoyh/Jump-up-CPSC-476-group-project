from flask import Flask, render_template, flash, request, url_for, redirect, session, jsonify
from wtforms import Form, TextField, validators, PasswordField, BooleanField
from passlib.hash import sha256_crypt
from psycopg2 import escape_string as thwart
import gc
from HopUp_Database_Code import connection
app = Flask(__name__)
app.secret_key = "super secret key"

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
@app.route('/dashboard/')
def dashboard_page():
    return render_template("explorer.html")


@app.route('/register/', methods=["GET", "POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            c, conn = connection()

            x = c.execute("SELECT * FROM users WHERE username = (%s)",
                          (thwart(username)))

            if int(x) > 0:
                flash('That username is already taken, please choose another')
                return render_template('register.html', form=form)

            else:
                c.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                          (thwart(username), thwart(password), thwart(email)))

                conn.commit()
                flash('Thanks for registering!')
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('dashboard_page'))

        return render_template("register.html", form=form)

    except Exception as e:
        return (str(e))



if __name__ == '__main__':
    app.run()
