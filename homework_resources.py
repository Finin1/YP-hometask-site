from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify
from data import db_session
from data.homework import Homework


def abort_if_day_not_found(code):
        session = db_session.create_session()
        date = code[0:2] + '.' + code[2:4] + '.' + code[4:6]
        form = code[6:]  
        homework_id = session.query(Homework.id).filter(Homework.date == date, Homework.form_id == form).first()
        if not homework_id:
            abort(404, message=f"Homework on {date} for {form} form not found")

class HomeworkResource(Resource):
    def get(self, code, subject):
        abort_if_day_not_found(code)
        date = code[0:2] + '.' + code[2:4] + '.' + code[4:6]
        form = code[6:]
        session = db_session.create_session()
        homework_id = session.query(Homework.id).filter(Homework.date == date, Homework.form_id == form).first()
        homework = session.query(Homework).get(homework_id[0])
        return jsonify({'homework': homework.to_dict(only=(f'subject{subject}', ))})
    
    def delete(self, code, subject):
        abort_if_day_not_found(code)
        session = db_session.create_session()
        date = code[0:2] + '.' + code[2:4] + '.' + code[4:6]
        form = code[6:]
        homework_id = session.query(Homework.id).filter(Homework.date == date, Homework.form_id == form).first()
        homework = session.query(Homework).get(homework_id[0])
        d = {1: homework.subject1, 2: homework.subject2, 3: homework.subject3, 4: homework.subject4, 5: homework.subject5,
             6: homework.subject6, 7: homework.subject7}
        d[subject] = ''
        
        if (not homework.subject1) and (not homework.subject4) and (not homework.subject5) and (not homework.subject6) and (not homework.subject7) and (not homework.subject2) and (not homework.subject3):
            session.delete(homework)
            session.commit() 
        return jsonify({'success': 'OK'})
    
    def post(self, code, subject):
        parser = reqparse.RequestParser()
        parser.add_argument('content', required=True)
        parser.add_argument('user_id', required=True, type=int)
        args = parser.parse_args()
        date = code[0:2] + '.' + code[2:4] + '.' + code[4:6]
        form = code[6:]
        session = db_session.create_session()
        homework_id = session.query(Homework.id).filter(Homework.date == date, Homework.form_id == form).first()
        if not homework_id:
            new_homework = Homework()
            new_homework.form_id = form
            new_homework.date = date
            match subject:
                case 1:
                    new_homework.subject1 = args['content']
                case 2:
                    new_homework.subject2 = args['content']
                case 3:
                    new_homework.subject3 = args['content']
                case 4:
                    new_homework.subject4 = args['content']
                case 5:
                    new_homework.subject5 = args['content']
                case 6:
                    new_homework.subject6 = args['content']
                case 7:
                    new_homework.subject7 = args['content']
            new_homework.edited_by = args['user_id']
            session.add(new_homework)
            session.commit()
            return jsonify({'id': new_homework.id})
        else:
            homework = session.query(Homework).get(homework_id[0])          
            match subject:
                case 1:
                    homework.subject1 = args['content']
                case 2:
                    homework.subject2 = args['content']
                case 3:
                    homework.subject3 = args['content']
                case 4:
                    homework.subject4 = args['content']
                case 5:
                    homework.subject5 = args['content']
                case 6:
                    homework.subject6 = args['content']
                case 7:
                    homework.subject7 = args['content']
            homework.edited_by = args['user_id']
            session.commit()
            return jsonify({'id': homework.id})         

class DayResourse(Resource):
    def get(self, code):
        abort_if_day_not_found(code)
        date = code[0:2] + '.' + code[2:4] + '.' + code[4:6]
        form = code[6:]
        session = db_session.create_session()
        homework_id = session.query(Homework.id).filter(Homework.date == date, Homework.form_id == form).first()
        homework = session.query(Homework).get(homework_id[0])
        return jsonify({'homework': homework.to_dict(only=('subject1', 'subject2', 'subject3', 'subject4', 'subject5', 'subject6', 'subject7'))})