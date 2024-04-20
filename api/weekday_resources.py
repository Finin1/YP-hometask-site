from flask_restful import reqparse, abort, Resource
from flask import jsonify
from data import db_session
from data.week_days import WeekDay


def abort_if_weekday_not_found(week_day_id):
    session = db_session.create_session()
    week_day = session.query(WeekDay).get(week_day_id)
    session.close()
    if not week_day:
        abort(404, message=f"Form {week_day_id} not found")


class WeekDayResource(Resource):
    def get(self, week_day_id):
        abort_if_weekday_not_found(week_day_id)
        session = db_session.create_session()
        week_day = session.query(WeekDay).get(week_day_id)
        session.close()
        return jsonify({"weekday": week_day.to_dict(only=('subject1', 'subject2', 'subject3', 'subject4', 'subject5', 'subject6', 'subject7'))})

    def delete(self, week_day_id):
        parser = reqparse.RequestParser()
        parser.add_argument("api_key", required=True)
        args = parser.parse_args()
        if args["api_key"] != '#|oQh8OSOXVwQTA36@x4jDbK':
            return abort(403, message="Wrong API key")
        abort_if_weekday_not_found(week_day_id)
        session = db_session.create_session()
        week_day = session.query(WeekDay).get(week_day_id)
        session.delete(week_day)
        session.commit()
        session.close()
        return jsonify({"success": "OK"})


class AllWeekDaysResource(Resource):
    def get(self):
        session = db_session.create_session()
        all_week_days = session.query(WeekDay).all()
        dict_for_json = {"week_days": []}
        for week_day in all_week_days:
            dict_form = week_day.to_dict()
            dict_for_json["forms"].append(dict_form)
        session.close()
        return jsonify(dict_for_json)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("subject1", required=True, type=int)
        parser.add_argument("subject2", required=True, type=int)
        parser.add_argument("subject3", required=True, type=int)
        parser.add_argument("subject4", required=True, type=int)
        parser.add_argument("subject5", required=True, type=int)
        parser.add_argument("subject6", required=True, type=int)
        parser.add_argument("subject7", required=True, type=int)
        args = parser.parse_args()
        session = db_session.create_session()
        new_week_day = WeekDay()
        new_week_day.subject1 = args["subject1"]
        new_week_day.subject2 = args["subject2"]
        new_week_day.subject3 = args["subject3"]
        new_week_day.subject4 = args["subject4"]
        new_week_day.subject5 = args["subject5"]
        new_week_day.subject6 = args["subject6"]
        new_week_day.subject7 = args["subject7"]
        session.add(new_week_day)
        session.commit()
        session.close()
        return jsonify({"id": new_week_day.id})
