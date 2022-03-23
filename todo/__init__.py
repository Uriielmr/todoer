import os    #Nos permite acceder a las variables de entorno

from flask import Flask

# from .auth import bp

# app = Flask(__name__)

def create_app():      #Esta funcion nos va a servir para crear testing o varias instancias en nuestra aplicacion
    app = Flask(__name__)           #Instancia de la clase flask o constructor

    app.config.from_mapping(    #Nos permite definir variables de configuracion que depues se van a poder utilizar en la app 
        SECRET_KEY='mikey',                       #Es una llave que nos va a permitir definir las sesiones en nuestra apliccion
        DATABASE_HOST=os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD=os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER=os.environ.get('FLASK_DATABASE_USER'),
        DATABASE=os.environ.get('FLASK_DATABASE')
    )
    from . import db

    db.init_app(app)

    from . import auth
    from . import todo

    app.register_blueprint(auth.bp)
    app.register_blueprint(todo.bp)

    @app.route('/hola')
    def hola():
        return 'Hola hooa hola'

    return app





# if __name__ == "__main__":
#   app.run(debug=True, port=4000) 