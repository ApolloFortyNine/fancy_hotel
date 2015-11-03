CREATE TABLE reservations (
  id SERIAL,
  reservation_id BIGINT NOT NULL,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  extra_bed_selected BOOLEAN NOT NULL DEFAULT false,
  is_cancelled BOOLEAN NOT NULL DEFAULT false,
  room_number_id INTEGER NOT NULL,
  location_id VARCHAR(30) NOT NULL,
  customer_id varchar(30) NOT NULL,
  card_number_id BIGINT,
  PRIMARY KEY (id),
  FOREIGN KEY (room_number_id, location_id) REFERENCES rooms(room_number, location),
  FOREIGN KEY (customer_id) REFERENCES customers(username),
  FOREIGN KEY (card_number_id) REFERENCES cards(card_number) ON DELETE SET NULL
);
