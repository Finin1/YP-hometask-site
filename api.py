import flask
from api import homework_resources, form_resources, weekday_resources, user_resources
from flask_restful import Api
from data import db_session

app = flask.Flask(__name__)
api = Api(app)

db_session.global_init("db/hometask_site.sqlite")
api.add_resource(
    homework_resources.HomeworkResource, "/api/homeworks/<code>/<int:subject>"
)
api.add_resource(homework_resources.AllHometaskForDayResource, "/api/homeworks/<code>")
api.add_resource(form_resources.FormResource, "/api/forms/<int:form_id>")
api.add_resource(form_resources.AllFormsResource, "/api/forms")
api.add_resource(weekday_resources.AllWeekDaysResource, "/api/weekdays")
api.add_resource(weekday_resources.WeekDayResource, "/api/weekdays/<int:week_day_id>")
api.add_resource(user_resources.UserResource, '/api/users/<int:user_id>')
api.add_resource(user_resources.AllUsersResource, '/api/users')

if __name__ == "__main__":
    app.run("127.0.0.1", port=5001)
