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

class EditForm(FlaskForm):
    text = StringField('Домашняя работа')
    submit = SubmitField('Сохранить')


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
    dates = None
    can_edit = False

    try:
        form = flask.session.get('form')
        if flask.session['login_key']:
            is_logged = True
            username = flask.session.get("username")
        else:
            flask.redirect('/login')
    except KeyError:
        flask.session['login_key'] = None
        flask.session.permanent = True
        flask.redirect('/login')    
    
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
        dates = []
        for i in range(6):
            print(i)
            s_curr_day = str(curr_day)
            code_for_ht = s_curr_day[8:] + s_curr_day[5:7] + s_curr_day[0:4] + str(form)
            dates.append([s_curr_day[8:], s_curr_day[5:7], s_curr_day[0:4]])
            homework_rs = request('get', f'http://127.0.0.1:5001/api/homeworks/{code_for_ht}')
            if homework_rs.status_code == 404:
                homework = {'subject1': '', 'subject2': '', 'subject3': '', 'subject4': '', 'subject5': '', 'subject6': '', 'subject7': ''}
            else:
                homework = homework_rs.json()['homework']
                print(homework)
            wd_id_rs = request('get', f'http://127.0.0.1:5001/api/forms/{form}')
            if wd_id_rs.status_code == 404:
                break
            else:
                wd_id = wd_id_rs.json()['form'][f'week_day{i + 1}']
            wd_schedule_rs = request('get', f'http://127.0.0.1:5001/api/weekdays/{wd_id}')
            if wd_schedule_rs.status_code == 404:
                break
            else:
                wd_schedule = wd_schedule_rs.json()['weekday']
            weekdays.append([wd_schedule, homework])
            curr_day += datetime.timedelta(days=1)
        print(weekdays)

        if flask.session.get('permition_lvl') == 1:
            can_edit = True
        else:
            can_edit = False

    return flask.render_template('main.html', is_logged=is_logged,
                                  username=username, weekdays=weekdays, zip=zip,
                                  title='Дневник', len=len, dates=dates, can_edit=can_edit,
                                  week=['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'])

@app.route('/edit/<date>/<int:subject>', methods=['GET', 'POST'])
def edit(date, subject):
    if flask.session.get('permition_lvl') == 1:
        form = EditForm()
        first_time = False
        fm_id = str(flask.session.get('form'))
        ht_response = request('get', f'http://127.0.0.1:5001/api/homeworks/{date + fm_id}/{subject}')
        if ht_response.status_code == 404:
            pass
        elif first_time:
            first_time = False
            form.text.data = ht_response.json()['homework'][f'subject{subject}']
        if form.validate_on_submit():
            print(form.text.data)
            edit_request = request('post', f'http://127.0.0.1:5001/api/homeworks/{date + fm_id}/{subject}', 
                                   json={'content': form.text.data, 'user_id': flask.session.get('user_id')})
            print(edit_request)
            return flask.redirect('/')
        return flask.render_template('edit.html', title='Редактирование д/з', form=form, date=date, is_logged=True,
                                     username=flask.session.get("username"))
    else:
        return flask.redirect('/')

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
            flask.session['user_id'] = user.id
            flask.session['permition_lvl'] = user.permition_level
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
    flask.session['user_id'] = None
    flask.session['permition_lvl'] = None
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