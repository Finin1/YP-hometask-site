from flask_restful import reqparse, abort, Resource
from flask import jsonify
from data import db_session
from data.users import User


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    session.close()
    if not user:
        abort(404, message=f"User {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.close()
        return jsonify({"user": user.to_dict(only=())})

    def delete(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument("api_key", required=True)
        args = parser.parse_args()
        if args["api_key"] != '#|oQh8OSOXVwQTA36@x4jDbK':
            return abort(403, message="Wrong API key")
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({"success": "OK"})


class AllUsersResource(Resource):
    def get(self):
        session = db_session.create_session()
        all_users = session.query(User).all()
        dict_for_json = {"users": []}
        for user in all_users:
            dict_form = user.to_dict()
            dict_for_json["users"].append(dict_form)
        session.close()
        return jsonify(dict_for_json)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("surname", required=True)
        parser.add_argument("name", required=True, type=int)
        parser.add_argument("nickname", required=True, type=int)
        parser.add_argument("hashed_password", required=True, type=int)
        parser.add_argument("permition_level", required=True, type=int)
        parser.add_argument("modified_date", required=True, type=int)
        parser.add_argument("form_id", required=True, type=int)
        args = parser.parse_args()
        session = db_session.create_session()
        new_user = User()
        new_user.surname = args["surname"]
        new_user.name = args["name"]
        new_user.nickname = args["nickname"]
        new_user.hashed_password = args["hashed_password"]
        new_user.permition_level = args["permition_level"]
        new_user.modified_date = args["modified_date"]
        new_user.form_id = args["form_id"]
        session.add(new_user)
        session.commit()
        session.close()
        return jsonify({"id": new_user.id})
