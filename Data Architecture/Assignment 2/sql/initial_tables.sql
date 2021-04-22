DROP TABLE IF EXISTS symbol, business,  exchange, instrument, symbol_business, daily_data CASCADE;
DROP TABLE IF EXISTS city, county, state, country, timezones CASCADE;

CREATE TABLE country(
id SERIAL PRIMARY KEY,
name TEXT UNIQUE NOT NULL,  
code TEXT NOT NULL
);

CREATE TABLE state(
id SERIAL PRIMARY KEY,
name TEXT UNIQUE NOT NULL, 
abbrev TEXT NULL,
country_id INTEGER NOT NULL,
FOREIGN KEY (country_id) REFERENCES country(id)
);

CREATE TABLE county(
id SERIAL PRIMARY KEY,
name TEXT NOT NULL, 
state_id INTEGER NOT NULL,
FOREIGN KEY (state_id) REFERENCES state(id)
);

CREATE TABLE timezones(
id SERIAL PRIMARY KEY,
name TEXT UNIQUE NOT NULL
);

CREATE TABLE city(
id SERIAL PRIMARY KEY,
name TEXT NOT NULL, 
county_id INTEGER NOT NULL,
timezone_id INTEGER NOT NULL,
FOREIGN KEY (county_id) REFERENCES county(id),
FOREIGN KEY (timezone_id) REFERENCES timezones(id)
);

CREATE TABLE exchange(
id SERIAL PRIMARY KEY,
abbrev TEXT NOT NULL,
name TEXT NULL,
created_date TIMESTAMP NOT NULL DEFAULT CURRENT_DATE,
last_updated_date TIMESTAMP NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE business(
id SERIAL PRIMARY KEY,
name TEXT UNIQUE NOT NULL,
city_id INTEGER NOT NULL,
sector TEXT NULL,
industry TEXT NULL,
website_url VARCHAR(255) NULL,
created_date TIMESTAMP NOT NULL DEFAULT CURRENT_DATE,
last_updated_date TIMESTAMP NOT NULL DEFAULT CURRENT_DATE,
FOREIGN KEY (city_id) REFERENCES city(id)
);

CREATE TABLE instrument(
id SERIAL PRIMARY KEY,
name TEXT UNIQUE NOT NULL,
belong_business BOOLEAN NOT NULL,
created_date TIMESTAMP NOT NULL DEFAULT CURRENT_DATE,
last_updated_date TIMESTAMP NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE symbol(
id SERIAL PRIMARY KEY,
exchange_id integer NOT NULL,
instrument_id integer NOT NULL,
ticker TEXT NOT NULL,
currency VARCHAR(64) NOT NULL,
created_date TIMESTAMP NOT NULL DEFAULT CURRENT_DATE,
last_updated_date TIMESTAMP NOT NULL DEFAULT CURRENT_DATE,
FOREIGN KEY (exchange_id) REFERENCES exchange(id),	
FOREIGN KEY (instrument_id) REFERENCES instrument(id)
);

CREATE TABLE symbol_business(
symbol_id integer,
business_id integer NOT NULL,
FOREIGN KEY (symbol_id) REFERENCES symbol(id),	
FOREIGN KEY (business_id) REFERENCES business(id),
UNIQUE(symbol_id, business_id)
);

CREATE TABLE daily_data(
id SERIAL PRIMARY KEY,
symbol_id INTEGER NOT NULL,
date_price DATE,
open_price NUMERIC NOT NULL,
high_price NUMERIC NOT NULL,
low_price NUMERIC NOT NULL,
close_price NUMERIC NOT NULL,
volume BIGINT NOT NULL,	
created_date TIMESTAMP NOT NULL DEFAULT CURRENT_DATE,
FOREIGN KEY (symbol_id) REFERENCES symbol(id)
);