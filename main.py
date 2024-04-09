import flask

app = flask.Flask('__main__')

@app.route('/')
@app.route('/main')
def main():
    is_logged = False 
    return flask.render_template('main.html', is_logged=is_logged)


if __name__ == '__main__':
    app.run('127.0.0.1', 5000)