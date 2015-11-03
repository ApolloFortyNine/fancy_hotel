CREATE TABLE cards (
  card_number VARCHAR(20) NOT NULL,
  name_on_card VARCHAR(50) NOT NULL,
  expiration_date DATE NOT NULL,
  cvv INT NOT NULL,
  customer_id VARCHAR(30) NOT NULL,
  PRIMARY KEY (card_number),
  FOREIGN KEY (customer_id) REFERENCES customers(username)
) Engine = InnoDB;
