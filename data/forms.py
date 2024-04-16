import sqlalchemy
from sqlalchemy import orm
from .db_session import  SqlAlchemyBase

class Form(SqlAlchemyBase):
    __tablename__ = 'forms'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    week_day1 = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey('week_days.id'))
    week_day2 = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey('week_days.id'))
    week_day3 = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey('week_days.id'))
    week_day4 = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey('week_days.id'))
    week_day5 = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey('week_days.id'))
    week_day6 = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey('week_days.id'))
    user = orm.relationship('User', back_populates='forms')
    Homework = orm.relationship('Homework', back_populates='forms')
    # week_days = orm.relationship('WeekDay', foreign_keys=[week_day1, week_day2, week_day3, week_day4, week_day5, week_day6])