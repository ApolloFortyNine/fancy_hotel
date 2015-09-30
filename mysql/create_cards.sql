CREATE TABLE cards (
  id SERIAL,
  name_on_card VARCHAR(50) NOT NULL,
  card_number INT NOT NULL,
  expiration_date DATE NOT NULL,
  cvv INT NOT NULL,
  user_id BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);
