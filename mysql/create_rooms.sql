CREATE TABLE rooms (
  room_number INTEGER NOT NULL,
  location VARCHAR(30) NOT NULL,
  room_category VARCHAR(20) NOT NULL,
  cost_per_day DOUBLE NOT NULL,
  cost_of_extra_bed_per_day DOUBLE NULL,
  persons_allowed INTEGER NOT NULL,
  PRIMARY KEY (room_number, location)
) Engine = InnoDB;
