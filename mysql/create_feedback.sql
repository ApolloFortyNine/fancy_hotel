CREATE TABLE feedback (
  id SERIAL,
  comment TEXT NULL,
  rating VARCHAR(20) NOT NULL,
  location VARCHAR(30) NOT NULL,
  customer_id BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (customer_id) REFERENCES customers(username)
);
