# fancy_hotel
Fancy Hotel web app for CS 4400

This query returns only rooms that are not reserved.

    SELECT * FROM rooms WHERE rooms.location='Atlanta' AND rooms.room_number NOT IN (SELECT room_number_id FROM (SELECT id FROM reservations WHERE ('2015-11-12' >= end_date) AND ('2015-11-10' <= start_date) AND is_cancelled=0) resv JOIN rooms_reservations rooms_resv ON resv.id=rooms_resv.reservation_id);
