from flask import Flask, render_template, request, session
from flask import redirect, url_for
from pymysql import connect

app = Flask(__name__)
app.secret_key = 'not_secret_at_all'

### Our username and password:
### cs4400_Group_26
### eOAsu3N4
### TODO MAKE SURE END DATE IS AFTER START DATE
###


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        conn = get_connection()
        c = conn.cursor()
        query_str = """SELECT username, password FROM customers WHERE username='{0}'""".format(request.form['username'])
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
        conn = get_connection()
        c = conn.cursor()
        query_str = """SELECT username FROM customers WHERE username='{0}'""".format(request.form['username'])
        c.execute(query_str)
        if c.fetchone():
            return 'Username taken'
        if request.form['password'] != request.form['confirm_password']:
            return "Password didn't match"
        query_str = """INSERT INTO customers (username, password, email)
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
    if request.method == 'POST':
        conn = get_connection()
        c = conn.cursor()
        req_start_date = request.form['start_date']
        req_end_date = request.form['end_date']
        session['start_date'] = req_start_date
        session['end_date'] = req_end_date
        req_loc = request.form['location']
        session['location'] = req_loc
        query_str = """
        SELECT * FROM rooms WHERE rooms.location='{0}' AND rooms.room_number NOT IN (SELECT room_number_id
        FROM (SELECT id FROM reservations WHERE ('{2}' >= end_date) AND ('{1}' <= start_date) AND
        is_cancelled=0) resv JOIN rooms_reservations rooms_resv ON resv.id=rooms_resv.reservation_id)
        """.format(req_loc, req_start_date, req_end_date)
        c.execute(query_str)
        result = c.fetchall()
        print(result)
        conn.close()
        return render_template('search_results.jinja', rooms=result)
    # This could be replaced with a list of locations, if we know all of them
    conn = get_connection()
    c = conn.cursor()
    query_str = """SELECT DISTINCT location FROM rooms"""
    c.execute(query_str)
    result = c.fetchall()
    conn.close()
    return render_template('search_rooms.jinja', locations=result)

@app.route('/select_results', methods=['POST'])
def select_results():
    if 'username' not in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        if 'rooms' not in request.form:
            return url_for('search_rooms')
        selected_rooms = request.form.getlist('rooms')
        extra_beds = []
        if 'extra_beds' in request.form:
            extra_beds = request.form.getlist('extra_beds')
        conn = get_connection()
        c = conn.cursor()
        total = 0
        rooms_arr = []
        for x in selected_rooms:
            query_str = """SELECT * FROM rooms WHERE room_number={0} AND location='{1}'""".format(x, session['location'])
            c.execute(query_str)
            result = c.fetchone()
            if x in extra_beds:
                total += result[4]
            total += result[3]
            rooms_arr.append(result)
        print(rooms_arr)
        session['selected_rooms'] = selected_rooms
        return str(request.form) + "Total: " + str(total)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

def get_connection():
    conn = connect(host='192.227.175.138',
                   user='fancy2',
                   password='bubbles',
                   db='fancy_phase_ii',
                   charset='utf8')
    return conn

if __name__ == '__main__':
    app.debug = True
    app.run("127.0.0.1", port=5000)
