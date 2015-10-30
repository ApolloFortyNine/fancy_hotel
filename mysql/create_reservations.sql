CREATE TABLE reservations (
  id SERIAL,
  reservation_id BIGINT NOT NULL,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  extra_bed_selected BOOLEAN NOT NULL DEFAULT false,
  room_id BIGINT UNSIGNED NOT NULL,
  customer_id VARCHAR(30) NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (room_id) REFERENCES rooms(id),
  FOREIGN KEY (customer_id) REFERENCES customers(username)
);
