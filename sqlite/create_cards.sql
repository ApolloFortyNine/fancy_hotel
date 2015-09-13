CREATE TABLE cards (
  id INTEGER NOT NULL,
  name_on_card TEXT NOT NULL,
  card_number INTEGER NOT NULL,
  expiration_date DATETIME NOT NULL,
  cvv INTEGER NOT NULL,
  user_id INTEGER,
  PRIMARY KEY (id),
  FOREIGN KEY("user_id") REFERENCES users (id)
);
