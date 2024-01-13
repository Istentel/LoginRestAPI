from web import app
from flask import render_template, redirect, url_for, jsonify, flash, session
from web.forms import RegisterForm, LoginForm
from web.db_api import register_user_api, login_user_api

@app.route('/api/hello', methods=['GET'])
def get_hello():
    return jsonify({'message': 'Hello from the server!'})

@app.route('/')
@app.route('/home')
def home_page():
    if not 'username' in session:
        return redirect(url_for("login_page"))
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():

        response = login_user_api(form.email.data, form.password.data)

        if response and response.status_code == 200:
            flash('Success! You logged in!', category='success')
            session["username"] = form.email.data
            return redirect(url_for('home_page'))
        else:
            flash('Username or password are not correct! Please try again!', category='danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = {'username': form.username.data, 'password': form.password1.data, 'email': form.email.data}

        response = register_user_api(new_user)
        
        if response:
            flash(f'Success! User {new_user["username"]} created succesfully!', category='success')
            session["username"] = form.email.data
            return render_template('home.html')
        else:
            return jsonify({'message': 'No valid response'}) 
    
    if form.errors != {}:
        for err_msj in form.errors.values():
            flash(f'Error when creating an user:{err_msj}', category='danger')

    return render_template('register.html', form=form)

@app.route("/logout")
def logout_page():
    session["username"] = None
    return redirect("/")

@app.route('/api/test', methods=['GET'])
def test():
    #response = requests.get('http://db_gateway:5001/api/hello')

    # new_user = {"username": "newuser", "password": "pass", "email": "emailtest"}

    # headers={
    #     'Content-type':'application/json', 
    #     'Accept':'application/json'
    # }

    #response = requests.post('http://db_gateway:5001/api/register', headers=headers, json=json.dumps(new_user))

    response = login_user_api("cristi233@yahoo.com", "passwordabc")

    if response and response.status_code == 200:
        print("Got here!")
        return response.content, response.status_code
    else:
        return jsonify({'message': 'No valid response'})
