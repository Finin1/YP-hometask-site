import flask
import homework_resources
from flask_restful import reqparse, abort, Api, Resource
from data import db_session

app = flask.Flask(__name__)
api = Api(app)

db_session.global_init('db/hometask_site.sqlite')
api.add_resource(homework_resources.HomeworkResource, '/api/<code>/<int:subject>')

if __name__ == '__main__':
    app.run('127.0.0.1', port=5001)