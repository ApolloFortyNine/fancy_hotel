from pymysql import connect

conn = connect(host='192.227.175.138',
               user='fancy',
               password='bubbles',
               db='fancy_hotel',
               charset='utf8')

curs = conn.cursor()
# MAY HAVE TO RETYPE CREATE TABLE FOR NO REASON WHEN COPY
# PASTING TABLE CREATE COMMANDS
# In order to trigger the pycharm weird highlight
# Maybe invisible character before first character, for some reason

# query = """INSERT INTO rooms (room_number, room_category, cost_per_day, location, cost_of_extra_bed_per_day, persons_allowed)
#            VALUES (102, 'Standard', 75.50, 'Atlanta', 15.00, 2)
# """

# query = """INSERT INTO reservations (reservation_id, start_date, end_date, room_id, user_id)
#            VALUES (2, '2015-10-02', '2015-10-03', 2, 1)"""

# query = """
# SELECT *
# FROM (SELECT * FROM rooms WHERE location='Atlanta') r
# LEFT JOIN (SELECT * FROM reservations WHERE ('{0}' >= start_date AND '{0}' < end_date) OR ('{1}' > start_date AND '{1}' < end_date)) e on e.room_id=r.id
# WHERE e.id IS NULL
# """.format('2015-9-30', '2015-10-03')
# query = """
# SELECT *
# FROM (SELECT * FROM rooms WHERE location='Atlanta') r
# LEFT JOIN (SELECT * FROM reservations) e on e.room_id=r.id
# """

# All hail the working date query
query = """
SELECT r.*
FROM (SELECT * FROM rooms WHERE location='Atlanta') r
LEFT JOIN (SELECT * FROM reservations WHERE ('{0}' < end_date) AND ('{1}' > start_date)) e on e.room_id=r.id
WHERE e.id IS NULL
""".format('2015-10-2', '2015-10-04')
curs.execute(query)
print(curs.fetchall())
curs.close()
conn.commit()

