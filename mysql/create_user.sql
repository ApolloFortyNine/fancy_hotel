CREATE TABLE users (
  id SERIAL,
  username varchar(30) NOT NULL UNIQUE,
  password varchar(30) NOT NULL,
  email varchar(50) NOT NULL,
  manager BOOLEAN NOT NULL DEFAULT false,
  PRIMARY KEY (id)
);
