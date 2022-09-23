from flask import redirect, render_template, request, flash, session
from flask_app import app
from flask_app.models.registro import Usuario
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/users',methods=['POST'])
def create_user():
    is_valid = Usuario.validate_usuario(request.form)

    if not is_valid:
        return redirect("/")
    nuevo = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form["password"]),
    }
    id = Usuario.save(nuevo)
    if not id:
        flash("Email already exists.","register")
        return redirect('/')
    session['username'] = request.form['first_name']
    session['usuario_id'] = id
    return redirect('/dashboard')


@app.route("/login",methods=['POST'])
def login():
    data = {
        "email": request.form['email']
    }
    user = Usuario.get_by_email(data)
    if not user:
        flash("Invalid Email/Password","login")
        return redirect("/")
    
    if not bcrypt.check_password_hash(user.password,request.form['password']):
        flash("Invalid Email/Password","login")
        return redirect("/")
    session['user_id'] = user.id
    return redirect('/dashboard')


@app.route('/dashboard')
def show_user():
    return render_template('show.html', usuario=session['username'])


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


