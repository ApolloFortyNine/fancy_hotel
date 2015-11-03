CREATE TABLE reservations (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  total_cost DOUBLE NOT NULL,
  is_cancelled BOOLEAN NOT NULL DEFAULT false,
  room_number_id INTEGER NOT NULL,
  location_id VARCHAR(30) NOT NULL,
  customer_id VARCHAR(30) NOT NULL,
  card_number_id VARCHAR(20),
  PRIMARY KEY (id),
  FOREIGN KEY (room_number_id, location_id) REFERENCES rooms(room_number, location),
  FOREIGN KEY (customer_id) REFERENCES customers(username),
  FOREIGN KEY (card_number_id) REFERENCES cards(card_number) ON DELETE SET NULL
) Engine = InnoDB;
