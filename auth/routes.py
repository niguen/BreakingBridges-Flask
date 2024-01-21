import functools
from flask import render_template, request, flash, redirect, url_for, session, g
import uuid
from auth import bp

from werkzeug.security import check_password_hash, generate_password_hash


class User():
    def __init__(self, name, password):
        self.name = name
        self.password = password

admin = User('admin', generate_password_hash('Provadis'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = admin

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':

        username = request.form['username'].lower()
        password = request.form['password']
        error = None
        user = None
    
        if username == 'admin':
            user = admin
        


        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.name
            return redirect(url_for('admin.index'))
        flash('Login failed')

    return render_template('auth/login.html')

@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("main.index"))


# @bp.route("/createUser", methods=('GET', 'POST'))
# def create_user():
#     if request.method == 'POST':

#         username = request.form['userName'].lower()
#         password1 = request.form['inputPassword1']
#         password2 = request.form['inputPassword2']
#         apiKey = request.form['cognigyApiKey']
        

#         error = None

#         if username is None or password1 is None or password2 is None or apiKey is None:
#             error = 'All fields are required'
        
#         elif password1 != password2:
#             error = 'Passwords do not match'
        
#         elif db.session.execute(db.select(User).where(User.name == username)).one_or_none() is not None:
#             error = 'Username already taken'


#         passwordHash = generate_password_hash(password1)
        


#         if error is None:

#             user = User(name = username, password = passwordHash, cognigyApiKey = apiKey)
#             db.session.add(user)
#             db.session.commit()
#             session.clear()
#             return redirect(url_for('main.index_sapcai'))
#         flash(f'ERROR while creating user: {error}')


#     return render_template('auth/createUser.html')