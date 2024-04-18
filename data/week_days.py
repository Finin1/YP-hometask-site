import sqlalchemy
from sqlalchemy import orm
from .db_session import  SqlAlchemyBase

class WeekDay(SqlAlchemyBase):
    __tablename__ = "week_days"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    subject1 = sqlalchemy.Column(sqlalchemy.String, default='None')
    subject2 = sqlalchemy.Column(sqlalchemy.String, default='None')
    subject3 = sqlalchemy.Column(sqlalchemy.String, default='None')
    subject4 = sqlalchemy.Column(sqlalchemy.String, default='None')
    subject5 = sqlalchemy.Column(sqlalchemy.String, default='None')
    subject6 = sqlalchemy.Column(sqlalchemy.String, default='None')
    subject7 = sqlalchemy.Column(sqlalchemy.String, default='None')

    # form = orm.relationship('Form', backref="week_days")

    def to_dict(self, only=()) -> dict:
        wd_dict = {'id': self.id, 'subject1': self.subject1, 'subject2': self.subject2, 
                   'subject3': self.subject3, 'subject4': self.subject4, 'subject5': self.subject5, 
                   'subject6': self.subject6, 'subject7': self.subject7}
        
        if only:
            filtered_dict = {}
            for selected in only:
                filtered_dict[selected] = wd_dict[selected]
            return filtered_dict
        else:
            return wd_dict