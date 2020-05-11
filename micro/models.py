import os
import datetime
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
import peewee as pw
from app import BASE_DIR



DATABASE = pw.SqliteDatabase(os.path.join(BASE_DIR,'dev.sqlite'))

class Users(UserMixin,pw.Model):
    id = pw.AutoField()
    first_name = pw.CharField(null=True)
    last_name = pw.CharField(null=True)
    email = pw.CharField(unique=True)
    password = pw.CharField(max_length=100)
    joined_at = pw.DateTimeField(default=datetime.datetime.now)
    is_admin = pw.BooleanField(default=False)


    @classmethod
    def create_user(cls,email, password, admin=False):
        try:
            with DATABASE.transaction():
                cls.create(
                    email=email,
                    password=generate_password_hash(password),
                    is_admin=admin)
        except pw.IntegrityError:
            raise ValueError("User already exists")
    
    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Users], safe=True)
    DATABASE.close()