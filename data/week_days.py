import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import  SqlAlchemyBase

class WeekDay(SqlAlchemyBase):
    __tablename__ = "week_days"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    fisrt_subject = sqlalchemy.Column(sqlalchemy.String, default='None')
    second_subject = sqlalchemy.Column(sqlalchemy.String, default='None')
    third_subject = sqlalchemy.Column(sqlalchemy.String, default='None')
    fourth_subject = sqlalchemy.Column(sqlalchemy.String, default='None')
    fifth_subject = sqlalchemy.Column(sqlalchemy.String, default='None')
    sixth_subject = sqlalchemy.Column(sqlalchemy.String, default='None')
    seventh_subject = sqlalchemy.Column(sqlalchemy.String, default='None')

