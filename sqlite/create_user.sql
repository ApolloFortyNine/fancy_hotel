CREATE TABLE users (
  id INTEGER,
  username TEXT NOT NULL,
  password TEXT NOT NULL,
  email TEXT NOT NULL,
  manager BOOLEAN DEFAULT false,
  PRIMARY KEY (id)
);
