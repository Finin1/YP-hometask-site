import sqlalchemy
from sqlalchemy import orm
from .db_session import  SqlAlchemyBase

class Range(SqlAlchemyBase):
    __tablename__ = 'range'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    start_date = sqlalchemy.Column(sqlalchemy.Date)
    end_date = sqlalchemy.Column(sqlalchemy.Date)
    template1 = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey('template.id'))
    template2 = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey('template.id'))
    template3 = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey('template.id'))
    template4 = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey('template.id'))
    template5 = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey('template.id'))
    template6 = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey('template.id'))
    priority =  sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey('template.id'))
    template = orm.relationship('Template')