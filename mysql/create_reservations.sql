CREATE TABLE reservations (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  total_cost DECIMAL(10,2) NOT NULL,
  is_cancelled BOOLEAN NOT NULL DEFAULT false,
  customer_id VARCHAR(30) NOT NULL,
  card_number_id VARCHAR(20),
  PRIMARY KEY (id),
  FOREIGN KEY (customer_id) REFERENCES customers(username),
  FOREIGN KEY (card_number_id) REFERENCES cards(card_number) ON DELETE SET NULL
) Engine = InnoDB;
