CREATE TABLE rooms (
  id INTEGER,
  room_number INTEGER NOT NULL,
  room_category TEXT NOT NULL,
  cost_per_day DOUBLE PRECISION NOT NULL,
  location TEXT NOT NULL,
  cost_of_extra_bed_per_day DOUBLE PRECISION NOT NULL,
  extra_bed_selected BOOLEAN DEFAULT false,
  persons_allowed INTEGER NOT NULL,
  PRIMARY KEY (id)
);
