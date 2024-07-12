"""Database table schema"""

CREATE TABLE doctor (
	id INTEGER NOT NULL,
	first_name VARCHAR NOT NULL,
	last_name VARCHAR NOT NULL,
	first_name_cn VARCHAR NOT NULL,
	last_name_cn VARCHAR NOT NULL,
	consultation_fee FLOAT,
	consultation_fee_detail VARCHAR NOT NULL,
	consultation_fee_detail_cn VARCHAR NOT NULL,
	phone VARCHAR NOT NULL,
	category_id INTEGER NOT NULL,
	price_range_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(category_id) REFERENCES category (id),
	FOREIGN KEY(price_range_id) REFERENCES pricerange (id)
)

CREATE TABLE pricerange (
	id INTEGER NOT NULL,
	range VARCHAR NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (range)
)

CREATE TABLE schedule (
	doctor_id INTEGER NOT NULL,
	day_in_week INTEGER NOT NULL,
	working_hours VARCHAR NOT NULL,
	PRIMARY KEY (doctor_id, day_in_week),
	FOREIGN KEY(doctor_id) REFERENCES doctor (id)
)

CREATE TABLE category (
	id INTEGER NOT NULL,
	name VARCHAR NOT NULL,
	name_cn VARCHAR NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (name),
	UNIQUE (name_cn)
)

CREATE TABLE address (
	doctor_id INTEGER NOT NULL,
	street VARCHAR NOT NULL,
	room VARCHAR,
	district VARCHAR NOT NULL,
	city VARCHAR NOT NULL,
	PRIMARY KEY (doctor_id),
	FOREIGN KEY(doctor_id) REFERENCES doctor (id)
)

CREATE TABLE addresscn (
	doctor_id INTEGER NOT NULL,
	street VARCHAR NOT NULL,
	room VARCHAR,
	district VARCHAR NOT NULL,
	city VARCHAR NOT NULL,
	PRIMARY KEY (doctor_id),
	FOREIGN KEY(doctor_id) REFERENCES doctor (id)
)

CREATE INDEX ix_address_district ON address (district)


-- static table data
insert into category (name, name_cn) values("General Practitioner", "普通门诊"), ("bone", "骨科");

insert into pricerange (range) values ("0-200"), ("201-400"), ("401-600");