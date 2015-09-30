CREATE TABLE feedback (
  id SERIAL,
  comment TEXT NULL,
  rating VARCHAR(20) NOT NULL,
  location VARCHAR(30) NOT NULL,
  user_id BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);
