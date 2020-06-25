from flask import Flask, render_template, request
from gensearch import gensearch
from datetime import datetime
from DBContMan import UseDatabase

app = Flask(__name__)

app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'Franklin',
                          'password': 'password',
                          'database': 'genappDB', }


def log_request(req: 'flask_request', res: str) -> None:
    """Creates a log of the search and adds it to the DB"""
    now = datetime.now()
    log_datetime = now.strftime('%b %d %Y, %I:%M %p')
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """Insert into genlog (time, byear, results) values (%s, %s, %s)"""
        cursor.execute(_SQL, (log_datetime,
                              int(req.form['birthyear']),
                              res,))


@app.route('/calculate', methods=['POST'])
def gengenerate() -> 'html':
    byear = int(request.form['birthyear'])
    results = gensearch(byear)
    if results == 'Baby Boomer':
        results = 'Generation Baby Boomer'
    elif results == 'Silent Generation':
        results = 'The Silent Generation'
    elif results == 'Millenial':
        results = ' Millenial'
    else:
        pass
    log_request(request, results)
    return render_template('results.html',
                           the_title='Results',
                           the_results=results,
                           the_byear=byear)


@app.route('/')
@app.route('/landing')
def landing_page() -> 'html':
    return render_template('landing.html', the_title="What's Your Generation?")


@app.route('/viewlog')
def view_the_log() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """SELECT time, byear, results from genlog"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()
    titles = ('Time', 'Year', 'Generation')
    return render_template('viewlog.html',
                           the_title='GenSearch Log',
                           the_row_titles=titles,
                           the_data=contents, )


if __name__ == '__main__':
    app.run(debug=True)
