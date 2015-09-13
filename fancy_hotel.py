from flask import Flask, render_template, request, session
from flask import redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'not_secret_at_all'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        conn = sqlite3.connect('fancy_hotel.db')
        c = conn.cursor()
        query_str = """SELECT username, password FROM users WHERE username='{0}'""".format(request.form['username'])
        c.execute(query_str)
        resp = c.fetchone()
        conn.close()
        if not resp:
            return 'Incorrect username or password'
        username = resp[0]
        password = resp[1]
        if (username == request.form['username']) and (password == request.form['password']):
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            return 'Incorrect username or password'
    if 'username' in session:
        return render_template('index.jinja', username=session['username'])
    return render_template('index_login.jinja')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        conn = sqlite3.connect('fancy_hotel.db')
        c = conn.cursor()
        query_str = """SELECT username FROM users WHERE username='{0}'""".format(request.form['username'])
        c.execute(query_str)
        if c.fetchone():
            return 'Username taken'
        if request.form['password'] != request.form['confirm_password']:
            return "Password didn't match"
        query_str = """INSERT INTO users (username, password, email)
                       VALUES ('{0}', '{1}', '{2}')""".format(request.form['username'],
                                                              request.form['password'],
                                                              request.form['email'])
        c.execute(query_str)
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('register.jinja')

@app.route('/search_rooms', methods=['GET', 'POST'])
def search_rooms():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('search_rooms.jinja', locations=['Atlanta'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.debug = True
    app.run("127.0.0.1", port=5000)
