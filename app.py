from flask import Flask
from models import db
from authorization import init_jwt, register, login, auth_route
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///users.db'
app.register_blueprint(auth_route, url_prefix='/auth')

db.init_app(app)
init_jwt(app)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()

