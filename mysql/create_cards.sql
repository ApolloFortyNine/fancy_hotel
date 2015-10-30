CREATE TABLE cards (
  card_number BIGINT NOT NULL,
  name_on_card VARCHAR(50) NOT NULL,
  expiration_date DATE NOT NULL,
  cvv INT NOT NULL,
  customer_id BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (card_number),
  FOREIGN KEY (customer_id) REFERENCES customers(username)
);
