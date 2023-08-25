# SIGBE
aplicatie web cu python si framework-ul Flask pentru dezvoltare web
pt baze de date postgreSQL
in pgAdmin4 2 tabele:

CREATE TABLE elevi(
  id SERIAL PRIMARY KEY,
  username VARCHAR2(50),
  password VARCHAR2(50),
  email VARCHAR2(100),
  nume VARCHAR2(50),
  prenume VARCHAR2(50),
  data_nasterii DATE,
  cnp VARCHAR2(100)
)

CREATE TABLE fisiere (
	id SERIAL PRIMARY KEY,
	filename TEXT NOT NULL,
	data BYTEA NOT NULL,
	elev_id INT REFERENCES elevi(id)
)
