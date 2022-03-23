import mysql.connector

import click    #nos permite ejecutar comandos en la terminal
from flask import current_app, g           #mantiene la aplicacion que estamos ejecutando y g es una variable que estara en toda la aplicacion y es reutilizables 
from flask.cli import with_appcontext       #permite axceder a las variables que se encuentran en la configuracion de la aplicacion 
from .schema import instructions            #va a contener todos los script que necesitamos para crear la base de datos


def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=current_app.config['DATABASE_HOST'],
            user=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASSWORD'],
            database=current_app.config['DATABASE'],
            
        )
        g.c = g.db.cursor(dictionary=True)
    return g.db, g.c

def close_db(e=None):                                     
    db = g.pop('db', None)

    if db is not None:
        db.close()

        
def init_db():
    db, c = get_db()

    for i in instructions:
        c.execute(i)
    
    db.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():                  #se encarga de ejecutar la logica para poder correr los script que tengamos usa la libreria click
    init_db()
    click.echo('Base de datos inicializada')

def init_app(app):
    app.teardown_appcontext(close_db)                     #aca sirve para cerrar el servidor despues de que haya hecho la petion a la base de datos
    app.cli.add_command(init_db_command)