import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import  SqlAlchemyBase

class Template(SqlAlchemyBase):
    __tablename__ = "template"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    fisrt_subject = sqlalchemy.Column(sqlalchemy.String, default='None')
    second_subject = sqlalchemy.Column(sqlalchemy.String, default='None')
    third_subject = sqlalchemy.Column(sqlalchemy.String, default='None')
    fourth_subject = sqlalchemy.Column(sqlalchemy.String, default='None')
    fifth_subject = sqlalchemy.Column(sqlalchemy.String, default='None')
    sixth_subject = sqlalchemy.Column(sqlalchemy.String, default='None')
    eventh_subject = sqlalchemy.Column(sqlalchemy.String, default='None')

