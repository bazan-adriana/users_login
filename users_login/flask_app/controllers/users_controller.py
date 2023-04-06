# ==== ROUTING  ====
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


# ==========  LOGIN PAGE  =======
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect("/dashboard")
    return render_template("index.html")



# =========     REGISTER   -- method --- ACTION  ==============
@app.route("/users/register", methods=['POST'])
def user_reg():
    print(request.form)
    if not User.validate(request.form):
        return redirect('/')
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])   # HASH the PW
    data = {                       # get the DATA dict ready with the hashed pw
        'first_name': request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password': hashed_pw
    }
# controller creates a user and displays it on dashboard
    id = User.create(data)             # pass the DATA dict to the User constructor
    session['user_id'] = id            # store the user_id in session
    return redirect("/dashboard")



# ========== DASHBOARD -- view -- =========
@app.route("/dashboard")
def dash():
    # route guard 
    if 'user_id' not in session:
        return redirect('/')
    #  grab the user
    data = {
        'id' : session['user_id']
    }
    logged_user = User.get_by_id(data)
    return render_template("dashboard.html",
                            logged_user = logged_user)



#   =====   LOGOUT  =====
@app.route('/logout')
def logout():
    del session['user_id']
    return redirect('/')



#   =====   LOGIN  =====
@app.route('/users/login', methods=['POST'])
def login():
    # data ={
    #     'email' : request.form['email']
    # }
    user_in_db = User.get_by_email(request.form)
    # if email not found
    if not user_in_db:              
        flash("invalid credentials", "log")
        return redirect('/')
    # check password
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("invalid credentials", "log")
        return redirect('/')
    # if it works
    session['user_id'] = user_in_db.id
        
    return redirect('/dashboard')