import functools  #Set de funcines 

from flask import(
    Blueprint, flash, g, render_template, request, url_for, session, redirect  # flash; funcion permite enviar mensajes a nuestras plantillas, blueprint; es una clase crea blueprint y son configurables
)                                                                              #g; variable reurilizable, render_template;renderizar plantillas
from werkzeug.security import check_password_hash, generate_password_hash           #check_password_hash verifica la contraseña que se ingresa es igual a otra y esta generate_password_hash encripta la contraseña que se esta enviando

from todo.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET','POST'])
def register():
    print(0)
    if request.method == 'POST':
        print(1)
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        db, c = get_db()
        error = None
        c.execute(
            'select id from user where username = %s', (username,)
        )
        if not username:
            error = 'Username es requerido'
        if not password:
            error = 'Password es requerido'
        elif c.fetchone() is not None:
            error = 'Usuario {} se encuentra registrado.'.format(username)

        if error is None:
            c.execute(
                'insert into user (username, password) values (%s, %s)',
                (username, generate_password_hash(password))
            )
            db.commit()

            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')
                                 
#_____________LOGIN

@bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None
        c.execute(
            'select * from user where username = %s', (username,)    #se le agrega una coma al final de user name porque es una tupla
        )    
        user = c.fetchone()
  
        if user is None:
            error = 'Usuario y/o contraseña invalida'
        elif not check_password_hash(user['password'], password):
            error = 'Usuario y/o contraseña invalida'

        if error is None:
            session.clear()
            session['user_id'] = user ['id']
            return redirect(url_for('todo.index'))
            # return redirect(url_for('todo.index'))
        
        flash(error)
    
    return render_template('auth/login.html')

# ------PROTEGER RUTAS---

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute(
            'select * from user where id = %s', (user_id,)
        )
        g.user = c.fetchone()                       #retorna una lista de diccionarios 


def login_required(view):                 #esta es una funcion decoradora
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    
    return wrapped_view
        
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))