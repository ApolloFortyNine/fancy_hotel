CREATE TABLE customers (
  username varchar(30),
  password varchar(30) NOT NULL,
  email varchar(50) NOT NULL,
  PRIMARY KEY (username)
) Engine = InnoDB;
