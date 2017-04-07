from flask import Flask, render_template

app=Flask(__name__)

@app.route('/')
def test():
    return "He He He!!I was just testing your patience level!!!??!!!"

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/login')
def login():
    return render_template("login.html")

if __name__=="__main__":
    app.run(debug=True)
