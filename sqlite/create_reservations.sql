CREATE TABLE reservations (
  id INTEGER,
  --Randomly generate a max size bigint number
  --Check to make sure its not already in the DB
  reservation_id INTEGER NOT NULL,
  start_date DATETIME NOT NULL,
  end_date DATETIME NOT NULL,
  room_id INTEGER,
  user_id INTEGER,
  PRIMARY KEY (id),
  FOREIGN KEY("user_id") REFERENCES users (id),
  FOREIGN KEY("room_id") REFERENCES rooms (id)
);
