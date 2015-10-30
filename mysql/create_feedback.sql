CREATE TABLE feedback (
  id SERIAL,
  comment TEXT NULL,
  rating VARCHAR(20) NOT NULL,
  location VARCHAR(30) NOT NULL,
  customer_id varchar(30) NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (customer_id) REFERENCES customers(username)
);
