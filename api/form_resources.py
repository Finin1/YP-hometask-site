from flask_restful import reqparse, abort, Resource
from flask import jsonify
from data import db_session
from data.forms import Form


def abort_if_form_not_found(form_id):
    session = db_session.create_session()
    form = session.query(Form).get(form_id)
    session.close()
    if not form:
        abort(404, message=f"Form {form_id} not found")


class FormResource(Resource):
    def get(self, form_id):
        abort_if_form_not_found(form_id)
        session = db_session.create_session()
        form = session.query(Form).get(form_id)
        session.close()
        return jsonify({"form": form.to_dict(only=())})

    def delete(self, form_id):
        parser = reqparse.RequestParser()
        parser.add_argument("api_key", required=True)
        args = parser.parse_args()
        if args["api_key"] != '#|oQh8OSOXVwQTA36@x4jDbK':
            return abort(403, message="Wrong API key")
        abort_if_form_not_found(form_id)
        session = db_session.create_session()
        form = session.query(Form).get(form_id)
        session.delete(form)
        session.commit()
        session.close()
        return jsonify({"success": "OK"})


class AllFormsResource(Resource):
    def get(self):
        session = db_session.create_session()
        all_forms = session.query(Form).all()
        dict_for_json = {"forms": []}
        for form in all_forms:
            dict_form = form.to_dict()
            dict_for_json["forms"].append(dict_form)
        session.close()
        return jsonify(dict_for_json)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True)
        parser.add_argument("week_day1", required=True, type=int)
        parser.add_argument("week_day2", required=True, type=int)
        parser.add_argument("week_day3", required=True, type=int)
        parser.add_argument("week_day4", required=True, type=int)
        parser.add_argument("week_day5", required=True, type=int)
        parser.add_argument("week_day6", required=True, type=int)
        args = parser.parse_args()
        session = db_session.create_session()
        new_form = Form()
        new_form.name = args["name"]
        new_form.week_day1 = args["week_day1"]
        new_form.week_day2 = args["week_day2"]
        new_form.week_day3 = args["week_day3"]
        new_form.week_day4 = args["week_day4"]
        new_form.week_day5 = args["week_day5"]
        new_form.week_day6 = args["week_day6"]
        session.add(new_form)
        session.commit()
        session.close()
        return jsonify({"id": new_form.id})
