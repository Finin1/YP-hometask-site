import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login.mixins import UserMixin 
from .db_session import SqlAlchemyBase

class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    nickname = sqlalchemy.Column(sqlalchemy.String, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    permition_level = sqlalchemy.Column(sqlalchemy.Integer)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)
    form_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('forms.id') )
    forms = orm.relationship('Form', foreign_keys=form_id)
    homework = orm.relationship('Homework', back_populates='users')

    def to_dict(self, only=()) -> dict:
        usr_dict = {'id': self.id, 'surname': self.surname, 'name': self.name, 
                   'nickname': self.nickname, 'hashed_password': self.hashed_password, 'permition_level': self.permition_level, 
                   'modified_date': self.modified_date, 'form_id': self.form_id}
        
        if only:
            filtered_dict = {}
            for selected in only:
                filtered_dict[selected] = usr_dict[selected]
            return filtered_dict
        else:
            return usr_dict
        
    def check_password(self, password):
        if self.hashed_password == password:
            return True
        else:
            return False