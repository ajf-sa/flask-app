import os
from flask import Flask
import models


BASE_DIR= os.path.dirname(os.path.realpath(__file__))

DEBUG = True
SECRET_KEY='thisissecretkey'

app = Flask(__name__)
app.config.from_object(__name__)
    

if __name__ == "__main__":
    with app.app_context():
        from views import *

    models.initialize()
    try:
        models.Users.create_user(
            email='a@a.a',
            password='0000',
            admin=True
        )
    except ValueError:
        pass
    app.run(host='0.0.0.0')
