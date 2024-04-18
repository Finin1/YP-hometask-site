import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class Homework(SqlAlchemyBase):
    __tablename__ = "homework"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    subject1 = sqlalchemy.Column(sqlalchemy.String, default='') 
    subject2 = sqlalchemy.Column(sqlalchemy.String, default='') 
    subject3 = sqlalchemy.Column(sqlalchemy.String, default='') 
    subject4 = sqlalchemy.Column(sqlalchemy.String, default='') 
    subject5 = sqlalchemy.Column(sqlalchemy.String, default='') 
    subject6 = sqlalchemy.Column(sqlalchemy.String, default='') 
    subject7 = sqlalchemy.Column(sqlalchemy.String, default='')
    form_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('forms.id') )
    edited_by = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    forms = orm.relationship('Form', foreign_keys=form_id)
    users = orm.relationship('User', foreign_keys=edited_by)
    
    def to_dict(self, only=()) -> dict:
        ht_dict = {'id': self.id, 'date': self.date, 'subject1': self.subject1, 'subject2': self.subject2, 
                   'subject3': self.subject3, 'subject4': self.subject4, 'subject5': self.subject5, 
                   'subject6': self.subject6, 'subject7': self.subject7, 'form_id': self.form_id,  'edited_by': self.edited_by}
        
        if only:
            filtered_dict = {}
            for selected in only:
                filtered_dict[selected] = ht_dict[selected]
            return filtered_dict
        else:
            return ht_dict