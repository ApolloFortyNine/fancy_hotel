CREATE TABLE rooms_reservations (
  reservation_id BIGINT UNSIGNED,
  room_number_id INTEGER NOT NULL,
  location_id VARCHAR(30) NOT NULL,
  extra_bed_selected BOOLEAN NOT NULL DEFAULT false,
  PRIMARY KEY (reservation_id, room_number_id, location_id),
  FOREIGN KEY (room_number_id, location_id) REFERENCES rooms(room_number, location),
  FOREIGN KEY (reservation_id) REFERENCES reservations(id)
) Engine = InnoDB;
