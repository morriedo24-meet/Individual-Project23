from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


config = {
  "apiKey": "AIzaSyBFqU7fSxnYJ8TtN6PBrX0EOcEmOsLnZv0",
  "authDomain": "morrie-pyrebase.firebaseapp.com",
  "projectId": "morrie-pyrebase",
  "storageBucket": "morrie-pyrebase.appspot.com",
  "messagingSenderId": "635855264485",
  "appId": "1:635855264485:web:a6ccd5eca7ff98edc3520c",
  "measurementId": "G-YT44VY8PDS",
  "databaseURL": "https://morrie-pyrebase-default-rtdb.europe-west1.firebasedatabase.app/"
}


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here

@app.route('/home', methods=['GET', 'POST'])
def home():
    UID = login_session['user']['localId']
    curr_user = db.child("Users").child(UID).get().val()
    # print(curr_user)
    curr_user = dict(curr_user)
    # print(curr_user)
    user_name = curr_user['name']
    return render_template("home.html", name = user_name)



@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            UID = login_session['user']['localId']
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']
        pass_confirm = request.form['password_confirm']
        name = request.form['full_name']
        username = request.form['user_name']
        age = int(request.form['age'])
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {"name": name, "email": email, "password": password, "user_name": username, "Age": age,
            "PassConfirm" : pass_confirm}
            db.child("Users").child(UID).set(user)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
    return render_template("signup.html")



# @app.route('/instrument', methods=['GET', 'POST'])
# def instrument():
#     if request.method == 'POST':
#         Genre = request.form['genre']
#         print(Genre)
#         return render_template("instrument.html",genre=Genre)
#     return render_template('inst_page.html')



@app.route('/sing', methods=['GET', 'POST'])
def sing():
    return render_template("sing.html")


@app.route('/inst_page/<string:type>', methods=['GET', 'POST'])
def inst_page(type):
    if request.method == 'POST':
        Genre = request.form[type]

        print(Genre)
        return render_template("inst_page.html",genre = Genre)
    Genre = ""
    return render_template('inst_page.html',genre = Genre)

#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)