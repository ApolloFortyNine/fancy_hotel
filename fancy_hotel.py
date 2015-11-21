from flask import Flask, render_template, request, session
from flask import redirect, url_for
from pymysql import connect
import datetime

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
        username = request.form['username']
        if not username[1:].isdigit() or username[0] != "C":
            return render_template("error.jinja", message="Username must follow the proper format! Cnnnn")
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
        req_start_date_dt = datetime.datetime.strptime(req_start_date, "%Y-%m-%d").date()
        print(req_start_date)
        print(req_start_date_dt)
        if req_start_date_dt < datetime.date.today():
            return render_template("error.jinja", message="Please pick a starting date in the future.")
        req_end_date = request.form['end_date']
        req_end_date_dt = datetime.datetime.strptime(req_end_date, "%Y-%m-%d").date()
        if req_end_date_dt < req_start_date_dt:
            return render_template("error.jinja", message="The end date can not be before the start date.")
        session['start_date'] = req_start_date
        session['end_date'] = req_end_date
        req_loc = request.form['location']
        session['location'] = req_loc
        query_str = """
        SELECT * FROM rooms WHERE rooms.location='{0}' AND rooms.room_number NOT IN (SELECT room_number_id
        FROM (SELECT id FROM reservations WHERE is_cancelled=0 AND (((start_date >= '{1}') AND (end_date <= '{2}')) OR ((end_date > '{1}')
        AND (start_date < '{2}')))) resv JOIN rooms_reservations rooms_resv
        ON resv.id=rooms_resv.reservation_id)
        """.format(req_loc, req_start_date, req_end_date)
        c.execute(query_str)
        result = c.fetchall()
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

@app.route('/payment_form', methods=['GET', 'POST'])
def payment_form():
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
        session['selected_rooms'] = selected_rooms
        session['selected_extra_beds'] = extra_beds
        session['total'] = float(total)
        query_str = """SELECT card_number FROM cards WHERE customer_id='{0}'""".format(session['username'])
        # query_str = """SELECT room_number FROM rooms"""
        c.execute(query_str)
        result = c.fetchall()
        credit_cards_arr = []
        for x in result:
            last_four = x[0][-4:]
            y = x + (last_four, )
            credit_cards_arr.append(y)
        conn.close()
        return render_template('payment_form.jinja', credit_cards=credit_cards_arr,
                               start_date=session['start_date'], end_date=session['end_date'], total=total)
    if request.method == 'GET':
        if 'added_card' not in session:
            return redirect(url_for('index'))
        conn = get_connection()
        c = conn.cursor()
        total = 0
        extra_beds = []
        selected_rooms = session['selected_rooms']
        extra_beds = session['selected_extra_beds']
        rooms_arr = []
        for x in selected_rooms:
            query_str = """SELECT * FROM rooms WHERE room_number={0} AND location='{1}'""".format(x, session['location'])
            c.execute(query_str)
            result = c.fetchone()
            if x in extra_beds:
                total += result[4]
            total += result[3]
            rooms_arr.append(result)
        query_str = """SELECT card_number FROM cards WHERE customer_id='{0}'""".format(session['username'])
        # query_str = """SELECT room_number FROM rooms"""
        c.execute(query_str)
        result = c.fetchall()
        credit_cards_arr = []
        for x in result:
            last_four = x[0][-4:]
            y = x + (last_four, )
            credit_cards_arr.append(y)
        conn.close()
        return render_template('payment_form.jinja', credit_cards=credit_cards_arr,
                               start_date=session['start_date'], end_date=session['end_date'], total=total)


@app.route('/add_card', methods=['GET', 'POST'])
def add_card():
    if 'username' not in session:
        return redirect(url_for('index'))
    if request.method == 'GET':
        conn = get_connection()
        c = conn.cursor()
        query_str = """SELECT card_number FROM cards WHERE customer_id='{0}'""".format(session['username'])
        c.execute(query_str)
        result = c.fetchall()
        credit_cards_arr = []
        for x in result:
            last_four = x[0][-4:]
            y = x + (last_four, )
            credit_cards_arr.append(y)
        conn.close()
        return render_template('add_card.jinja', credit_cards=credit_cards_arr)
    if request.method == 'POST':
        conn = get_connection()
        c = conn.cursor()
        if 'credit_card_del' in request.form:
            query_str = """DELETE FROM cards WHERE card_number='{0}'""".format(request.form['credit_card_del'])
            c.execute(query_str)
            conn.commit()
            return redirect(url_for('index'))
        query_str = """INSERT INTO cards (card_number, name_on_card, expiration_date, cvv, customer_id)
                       VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')""".format(request.form['card_number'],
                                                                            request.form['card_name'],
                                                                            request.form['card_exp_date'],
                                                                            request.form['card_cvv'],
                                                                            session['username'])
        c.execute(query_str)
        conn.commit()
        conn.close()
        session['added_card'] = 1
        if 'total' not in session:
            print()
            return redirect(url_for('index'))
        return redirect(url_for('payment_form'))


@app.route('/make_reservation', methods=['POST'])
def make_reservation():
    if 'username' not in session:
        return redirect(url_for('index'))
    if 'credit_card' not in request.form:
        return redirect(url_for('index'))
    if request.method == 'POST':
        conn = get_connection()
        c = conn.cursor()
        query_str = """INSERT INTO reservations (start_date, end_date, total_cost, customer_id, card_number_id)
                       VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')""".format(session['start_date'],
                                                                            session['end_date'],
                                                                            session['total'],
                                                                            session['username'],
                                                                            request.form['credit_card'])
        c.execute(query_str)
        conn.commit()
        query_str = """SELECT LAST_INSERT_ID()"""
        c.execute(query_str)
        conn.commit()
        reservation_id = c.fetchone()[0]
        extra_beds = session['selected_extra_beds']
        select_extra_bed = 0
        for x in session['selected_rooms']:
            if x in extra_beds:
                select_extra_bed = 1
            query_str = """INSERT INTO rooms_reservations (reservation_id, room_number_id, location_id, extra_bed_selected)
                           VALUES ('{0}', '{1}', '{2}', '{3}')""".format(reservation_id,
                                                                         x,
                                                                         session['location'],
                                                                         select_extra_bed)
            c.execute(query_str)
            conn.commit()
        conn.close()
        username = session['username']
        session.clear()
        session['username'] = username
        return render_template("make_reservation.jinja", reservation_id=reservation_id)


@app.route('/cancel_search', methods=['GET', 'POST'])
def cancel_search():
    if request.method == 'GET':
        return render_template("cancel_search.jinja", type="Cancel")
    if request.method == 'POST':
        reservation_id = request.form['reservation_id']
        conn = get_connection()
        c = conn.cursor()
        query_str = """SELECT * FROM reservations WHERE id={0}""".format(reservation_id)
        c.execute(query_str)
        reservation_info = c.fetchone()
        start_date = reservation_info[1]
        end_date = reservation_info[2]
        todays_date = datetime.date.today()
        days_between = (start_date - todays_date).days
        total = reservation_info[3]
        is_cancelled = reservation_info[4]
        if is_cancelled == 1:
            return render_template("error.jinja", message="Already cancelled!")
        if days_between >= 3:
            refund = total
        elif days_between > 1:
            refund = 0.8 * total
        else:
            refund = 0

        query_str = """SELECT r.room_number_id, rooms.room_category, rooms.persons_allowed, rooms.cost_per_day,
                       rooms.cost_of_extra_bed_per_day, r.extra_bed_selected  FROM rooms_reservations r
                       JOIN rooms ON rooms.room_number=r.room_number_id AND rooms.location=r.location_id WHERE reservation_id={0}""".format(reservation_id)
        c.execute(query_str)
        result = c.fetchall()
        print(result)
        conn.close()
        return render_template("cancel_results.jinja",
                               start_date=start_date,
                               end_date=end_date,
                               todays_date=todays_date,
                               refund=refund,
                               total=total,
                               rooms=result,
                               reservation_id=reservation_id)


@app.route('/cancel_reservation', methods=['POST'])
def cancel_reservation():
    conn = get_connection()
    c = conn.cursor()
    query_str = """UPDATE reservations SET is_cancelled=1 WHERE id={0}""".format(request.form['reservation_id'])
    c.execute(query_str)
    conn.commit()
    conn.close()
    return render_template("cancel_reservation.jinja", reservation_id=request.form['reservation_id'])


@app.route('/update_search', methods=['GET', 'POST'])
def update_search():
    if request.method == 'GET':
        return render_template("cancel_search.jinja", type="Update")
    if request.method == 'POST':
        reservation_id = request.form['reservation_id']
        conn = get_connection()
        c = conn.cursor()
        query_str = """SELECT * FROM reservations WHERE id={0}""".format(reservation_id)
        c.execute(query_str)
        reservation_info = c.fetchone()
        curr_start_date = reservation_info[1]
        curr_end_date = reservation_info[2]
        is_cancelled = reservation_info[4]
        if is_cancelled == 1:
            return render_template("error.jinja", message="Already cancelled!")

        return render_template("update_choose.jinja", curr_start_date=curr_start_date, curr_end_date=curr_end_date, reservation_id=reservation_id)


@app.route('/update_results', methods=['POST'])
def update_results():
    conn = get_connection()
    c = conn.cursor()
    new_start_date = request.form['new_start_date']
    new_end_date = request.form['new_end_date']
    reservation_id = request.form['reservation_id']
    todays_date = datetime.date.today()
    new_start_date_dt = datetime.datetime.strptime(new_start_date, "%Y-%m-%d").date()
    new_end_date_dt = datetime.datetime.strptime(new_end_date, "%Y-%m-%d").date()
    if new_start_date_dt < todays_date:
        return render_template("error.jinja", message="Please pick a starting date in the future.")
    if new_end_date_dt < new_start_date_dt:
        return render_template("error.jinja", message="The end date can not be before the start date.")
    session['new_start_date'] = new_start_date
    session['new_end_date'] = new_end_date
    query_str = """SELECT r.room_number_id, rooms.room_category, rooms.persons_allowed, rooms.cost_per_day,
                   rooms.cost_of_extra_bed_per_day, r.extra_bed_selected FROM rooms_reservations r
                   JOIN rooms ON rooms.room_number=r.room_number_id AND rooms.location=r.location_id WHERE reservation_id={0} AND r.room_number_id NOT IN (SELECT room_number_id
                   FROM (SELECT id FROM reservations WHERE is_cancelled=0 AND (((start_date >= '{1}') AND (end_date <= '{2}')) OR ((end_date > '{1}')
                   AND (start_date < '{2}')))) resv JOIN rooms_reservations rooms_resv
                   ON resv.id=rooms_resv.reservation_id)""".format(reservation_id, new_start_date, new_end_date)
    c.execute(query_str)
    rooms_available = c.fetchall()

    query_str = """SELECT count(room_number_id) FROM rooms_reservations WHERE reservation_id={0}""".format(reservation_id)
    c.execute(query_str)
    num_rooms_booked = c.fetchone()[0]
    if num_rooms_booked != len(rooms_available):
        return render_template("error.jinja", message="Your previously booked rooms are not available on those days. Please cancel and remake the reservation.")

    query_str = """SELECT total_cost FROM reservations WHERE id={0}""".format(reservation_id)
    c.execute(query_str)
    total = c.fetchone()[0]
    conn.close()
    return render_template("update_results.jinja", rooms=rooms_available, reservation_id=reservation_id, total=total)


@app.route('/update_reservation', methods=['POST'])
def update_reservation():
    reservation_id = request.form['reservation_id']
    conn = get_connection()
    c = conn.cursor()
    query_str = """UPDATE reservations SET start_date='{0}', end_date='{1}' WHERE id={2}""".format(session['new_start_date'], session['new_end_date'], reservation_id)
    c.execute(query_str)
    conn.commit()
    conn.close()
    username = session['username']
    session.clear()
    session['username'] = username
    return render_template("update_reservation.jinja", reservation_id=reservation_id)


@app.route('/view_reviews', methods=['GET', 'POST'])
def view_reviews():
    if 'username' not in session:
        return redirect(url_for('index'))
    if request.method == 'GET':
        conn = get_connection()
        c = conn.cursor()
        query_str = """SELECT DISTINCT location FROM rooms"""
        c.execute(query_str)
        locations = c.fetchall()
        conn.close()
        return render_template("select_reviews_location.jinja", locations=locations)
    if request.method == 'POST':
        conn = get_connection()
        c = conn.cursor()
        location = request.form['location']

        query_str = """SELECT rating, comment FROM feedback WHERE location='{0}'""".format(location)
        c.execute(query_str)
        reviews = c.fetchall()
        conn.close()
        return render_template("view_reviews.jinja", location=location, reviews=reviews)


@app.route('/add_review', methods=['GET', 'POST'])
def add_review():
    if 'username' not in session:
        return redirect(url_for('index'))
    if request.method == 'GET':
        conn = get_connection()
        c = conn.cursor()
        query_str = """SELECT DISTINCT location FROM rooms"""
        c.execute(query_str)
        locations = c.fetchall()
        conn.close()
        return render_template('/add_review.jinja', locations=locations)
    if request.method == 'POST':
        conn = get_connection()
        c = conn.cursor()
        review = request.form['review']
        rating = request.form['rating']
        location = request.form['location']
        username = session['username']
        query_str = """INSERT INTO feedback (comment, rating, location, customer_id)
                       VALUES ('{0}', '{1}', '{2}', '{3}')""".format(review, rating, location, username)
        c.execute(query_str)
        conn.commit()
        conn.close()
        return render_template("added_review.jinja")


@app.route('/view_reservations_report', methods=['GET'])
def view_reservations_report():
    # We only have to hard code August and September
    # https://piazza.com/class/idhxg1pbj4w7bs?cid=170
    conn = get_connection()
    c = conn.cursor()

    # TODO Switch these dates to '2015-08-01' to '2015-09-30'
    query_str = """SELECT MONTH(r.start_date) AS mnth, r.location_id,
                   COUNT(DISTINCT r.id) AS reservations
                   FROM (SELECT id, start_date, room_number_id, location_id FROM reservations JOIN rooms_reservations ON rooms_reservations.reservation_id=reservations.id WHERE is_cancelled=0) r
                   WHERE start_date >= '2015-11-01' AND start_date <= '2015-12-31'
                   GROUP BY MONTH(r.start_date), r.location_id"""
    c.execute(query_str)
    result_pre_converted = c.fetchall()
    result = []
    k = 0
    # Convert month number to string, using November and December for testing
    for x in result_pre_converted:
        result.append(list(x))
        if result[k][0] == 11:
            result[k][0] = "November"
        elif result[k][0] == 12:
            result[k][0] = "December"
        elif result[k][0] == 8:
            result[k][0] = "August"
        elif result[k][0] == 9:
            result[k][0] = "September"
        k += 1

    conn.close()
    return render_template("view_reservations_report.jinja", result=result)

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
