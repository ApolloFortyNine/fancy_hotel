CREATE TABLE feedback (
  id INTEGER,
  comment TEXT,
  rating TEXT NOT NULL,
  location TEXT NOT NULL,
  user_id INTEGER,
  PRIMARY KEY (id),
  FOREIGN KEY("user_id") REFERENCES users (id)
)
