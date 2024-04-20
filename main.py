import flask
import datetime
from data import db_session
from data.users import User
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from requests import request


class LoginForm(FlaskForm):
    nickname = StringField('Имя пользователя', validators=[DataRequired()])
    # name = StringField('Имя', validators=[DataRequired()])
    # surname = StringField('Фамилия', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

db_session.global_init('db/hometask_site.sqlite')

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)

@app.route('/')
@app.route('/main')
def main():
    is_logged = False
    username = None   
    weekdays = None
    
    try:
        form = flask.session.get('form')
        if flask.session['login_key']:
            is_logged = True
            username = flask.session.get("username")
    except KeyError:
        flask.session['login_key'] = None
        flask.session.permanent = True
    
    if form:
        try:
            curr_first_weekday = datetime.date.fromisoformat(flask.session['current_first_week_day'])
        except KeyError:
            curr_first_weekday = datetime.date.today()
            while curr_first_weekday.weekday() != 0:
                curr_first_weekday -= datetime.timedelta(days=1)
            flask.session['current_first_week_day'] = datetime.date.isoformat(curr_first_weekday)
        curr_day = curr_first_weekday
        weekdays = []
        for i in range(6):
            print(i)
            s_curr_day = str(curr_day)
            code_for_ht = s_curr_day[8:] + s_curr_day[5:7] + s_curr_day[0:4] + str(form)
            print(code_for_ht)
            homework_rt = request('get', f'http://127.0.0.1:5001/api/homeworks/{code_for_ht}')
            if homework_rt.status_code == 404:
                break
            else:
                homework = homework_rt.json()['homework']
                print(homework)
            wd_id_rt = request('get', f'http://127.0.0.1:5001/api/forms/{form}')
            if wd_id_rt.status_code == 404:
                break
            else:
                wd_id = wd_id_rt.json()['form'][f'week_day{i + 1}']
            wd_schedule_rt = request('get', f'http://127.0.0.1:5001/api/weekdays/{wd_id}')
            if wd_schedule_rt.status_code == 404:
                break
            else:
                wd_schedule = wd_schedule_rt.json()['weekday']
            weekdays.append([wd_schedule, homework])
            curr_day += datetime.timedelta(days=1)
        print(weekdays)
    return flask.render_template('main.html', is_logged=is_logged,
                                  username=username, weekdays=weekdays, zip=zip,
                                  title='Дневник')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        print(type(form.nickname.data))
        user = db_sess.query(User).filter(User.nickname == form.nickname.data).first()
        print(1)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flask.session['login_key'] = 1236547890
            flask.session['username'] = user.name + ' ' + user.surname 
            flask.session['form'] = user.form_id
            return flask.redirect("/")
        return flask.render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    print(form.errors)
    return flask.render_template('login.html', title='Авторизация', form=form)

@app.route('/logout')
@login_required
def logout():
    flask.session['login_key'] = None
    flask.session['username'] = None 
    flask.session['form'] = None
    logout_user()
    return flask.redirect('/')

@app.route('/next')
def next_pg():
    flask.session['current_first_week_day'] = datetime.date.isoformat(datetime.date.fromisoformat(flask.session['current_first_week_day']) + datetime.timedelta(days=7))
    return flask.redirect('/')

@app.route('/prev')
def prev_pg():
    flask.session['current_first_week_day'] = datetime.date.isoformat(datetime.date.fromisoformat(flask.session['current_first_week_day']) - datetime.timedelta(days=7))
    return flask.redirect('/')

if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True)