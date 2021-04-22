
-- other tables

CREATE TABLE county(idcounty bigint, county text, area bigint, density decimal(10,2), province text);
CREATE TABLE authority(idauth serial not null, name text, idregion bigint);
CREATE TABLE region(idregion bigint, region text);
CREATE TABLE crime_type(idtype serial, type text);
CREATE TABLE income_type(idtype serial, type text, unit text);
CREATE TABLE sex(idsex serial, sex text);


\COPY county FROM 'county.csv' CSV HEADER;

INSERT INTO authority(name) SELECT DISTINCT county_region FROM initial_income_data d LEFT JOIN county c ON c.county = d.county_region WHERE c.idcounty is null or county = 'Dublin' ORDER BY county_region;
INSERT INTO region(idregion, region) SELECT idauth, name FROM authority WHERE name IN ('Northern and Western', 'Southern', 'Eastern and Midland');

UPDATE authority SET idregion = 1 WHERE name IN ('Border', 'West');
UPDATE authority SET idregion = 2 WHERE name IN ('South-East', 'South-West', 'Mid-West');
UPDATE authority SET idregion = 11 WHERE name IN ('Mid-East', 'Midland', 'Dublin');
DELETE FROM authority WHERE idregion IS NULL;

ALTER TABLE county ADD COLUMN idauth bigint;
UPDATE county SET idauth = (SELECT DISTINCT idauth FROM authority WHERE name = 'South-West') WHERE county IN ('Cork', 'Kerry');
UPDATE county SET idauth = (SELECT DISTINCT idauth FROM authority WHERE name = 'Border') WHERE county IN ('Cavan', 'Donegal', 'Leitrim', 'Monaghan', 'Sligo');
UPDATE county SET idauth = (SELECT DISTINCT idauth FROM authority WHERE name = 'Midland') WHERE county IN ('Laois', 'Longford', 'Offaly', 'Westmeath');
UPDATE county SET idauth = (SELECT DISTINCT idauth FROM authority WHERE name = 'West') WHERE county IN ('Galway', 'Mayo', 'Roscommon');
UPDATE county SET idauth = (SELECT DISTINCT idauth FROM authority WHERE name = 'Dublin') WHERE county IN ('Dublin');
UPDATE county SET idauth = (SELECT DISTINCT idauth FROM authority WHERE name = 'Mid-East') WHERE county IN ('Kildare', 'Louth', 'Meath', 'Wicklow');
UPDATE county SET idauth = (SELECT DISTINCT idauth FROM authority WHERE name = 'Mid-West') WHERE county IN ('Clare', 'Limerick', 'Tipperary');
UPDATE county SET idauth = (SELECT DISTINCT idauth FROM authority WHERE name = 'South-East') WHERE county IN ('Carlow', 'Kilkenny', 'Waterford', 'Wexford');
DELETE FROM county WHERE idauth IS NULL;

INSERT INTO crime_type(type) SELECT DISTINCT type_offece FROM transformed_crime_data;

ALTER TABLE transformed_crime_data ADD COLUMN idcounty bigint not null DEFAULT 0;

UPDATE transformed_crime_data SET idcounty = (SELECT idcounty FROM county WHERE county = 'Cork') where station_division like '%Cork%';
UPDATE transformed_crime_data SET idcounty = (SELECT idcounty FROM county WHERE county = 'Galway') where station_division like '%Galway%';
UPDATE transformed_crime_data SET idcounty = (SELECT idcounty FROM county WHERE county = 'Mayo') where station_division like '%Mayo%';
UPDATE transformed_crime_data SET idcounty = (SELECT idcounty FROM county WHERE county = 'Donegal') where station_division like '%Donegal%';
UPDATE transformed_crime_data SET idcounty = (SELECT idcounty FROM county WHERE county = 'Kerry') where station_division like '%Kerry%';
UPDATE transformed_crime_data SET idcounty = (SELECT idcounty FROM county WHERE county = 'Tipperary') where station_division like '%Tipperary%';
UPDATE transformed_crime_data SET idcounty = (SELECT idcounty FROM county WHERE county = 'Clare') where station_division like '%Clare%';
UPDATE transformed_crime_data SET idcounty = (SELECT idcounty FROM county WHERE county = 'Tyrone') where station_division like '%Tyrone%';
UPDATE transformed_crime_data SET idcounty = (SELECT idcounty FROM county WHERE county = 'Antrim') where station_division like '%Antrim%';
UPDATE transformed_crime_data SET idcounty = (SELECT idcounty FROM county WHERE county = 'Limerick') where station_division like '%Limerick%';
UPDATE transformed_crime_data SET idcounty = (SELECT idcounty FROM county WHERE county = 'Roscommon') where station_division like '%Roscommon%';
UPDATE transformed_crime_data SET idcounty = (SELECT idcounty FROM county WHERE county = 'Down') where station_division like '%Down%';
UPDATE transformed_crime_data SET idcounty = (SELECT idcounty FROM county WHERE county = 'Wexford') where station_division like '%Wexford%';
UPDATE transformed_crime_data SET idcounty = (SELECT idcounty FROM county WHERE county = 'Meath') where station_division like '%Meath%';
UPDATE transformed_crime_data SET idcounty = (SELECT idcounty FROM county WHERE county = 'Londonderry') where station_division like '%Londonderry%';
UPDATE transformed_crime_data SET idcounty = (SELECT idcounty FROM county WHERE county = 'Kilkenny') where station_division like '%Kilkenny%';
UPDATE transformed_crime_data SET idcounty = (SELECT idcounty FROM county WHERE county = 'Wicklow') where station_division like '%Wicklow%';
UPDATE transformed_crime_data SET idcounty = (SELECT idcounty FROM county WHERE county = 'Offaly') where station_division like '%Offaly%';
UPDATE transformed_crime_data SET idcounty = (SELECT idcounty FROM county WHERE county = 'Cavan') where station_division like '%Cavan%';
UPDATE transformed_crime_data SET idcounty = (SELECT idcounty FROM county WHERE county = 'Waterford') where station_division like '%Waterford%';
UPDATE transformed_crime_data SET idcounty = (SELECT idcounty FROM county WHERE county = 'Westmeath') where station_division like '%Westmeath%';
UPDATE transformed_crime_data SET idcounty = (SELECT idcounty FROM county WHERE county = 'Sligo') where station_division like '%Sligo%';
UPDATE transformed_crime_data SET idcounty = (SELECT idcounty FROM county WHERE county = 'Laois') where station_division like '%Laois%';
UPDATE transformed_crime_data SET idcounty = (SELECT idcounty FROM county WHERE county = 'Kildare') where station_division like '%Kildare%';
UPDATE transformed_crime_data SET idcounty = (SELECT idcounty FROM county WHERE county = 'Fermanagh') where station_division like '%Fermanagh%';
UPDATE transformed_crime_data SET idcounty = (SELECT idcounty FROM county WHERE county = 'Leitrim') where station_division like '%Leitrim%';
UPDATE transformed_crime_data SET idcounty = (SELECT idcounty FROM county WHERE county = 'Armagh') where station_division like '%Armagh%';
UPDATE transformed_crime_data SET idcounty = (SELECT idcounty FROM county WHERE county = 'Monaghan') where station_division like '%Monaghan%';
UPDATE transformed_crime_data SET idcounty = (SELECT idcounty FROM county WHERE county = 'Longford') where station_division like '%Longford%';
UPDATE transformed_crime_data SET idcounty = (SELECT idcounty FROM county WHERE county = 'Dublin') where station_division like '%Dublin%';
UPDATE transformed_crime_data SET idcounty = (SELECT idcounty FROM county WHERE county = 'Carlow') where station_division like '%Carlow%';
UPDATE transformed_crime_data SET idcounty = (SELECT idcounty FROM county WHERE county = 'Louth') where station_division like '%Louth%';
DELETE FROM transformed_crime_data WHERE idcounty = 0 OR station_division like '%/%';

ALTER TABLE transformed_crime_data ADD COLUMN idtype bigint;
UPDATE transformed_crime_data SET idtype = t.idtype FROM crime_type t WHERE t.type = transformed_crime_data.type_offence;

CREATE TABLE garda_station as SELECT DISTINCT id_station as idstation, station, idcounty FROM transformed_crime_data;


ALTER TABLE transformed_crime_data DROP COLUMN type_offence;
ALTER TABLE transformed_crime_data DROP COLUMN unit;
ALTER TABLE transformed_crime_data DROP COLUMN station_division;
ALTER TABLE transformed_crime_data DROP COLUMN station;
ALTER TABLE transformed_crime_data DROP COLUMN idcounty;


-- remove not needed, since state is addition of all other counties.
DELETE FROM transformed_population_data WHERE county = 'State';
DELETE FROM transformed_population_data WHERE sex = 'Both sexes';
ALTER TABLE transformed_population_data ADD COLUMN idcounty bigint;

UPDATE transformed_population_data SET idcounty = c.idcounty FROM county c WHERE transformed_population_data.county = c.county;
ALTER TABLE transformed_population_data DROP COLUMN county;
ALTER TABLE transformed_population_data DROP COLUMN statistic;
ALTER TABLE transformed_population_data DROP COLUMN unit;


INSERT INTO income_type(type) SELECT DISTINCT statistic FROM initial_income_data;


ALTER TABLE initial_income_data ADD COLUMN idtype;
ALTER TABLE initial_income_data ADD COLUMN idtype bigint not null DEFAULT 0;
UPDATE initial_income_data SET idtype = i.idtype FROM income_type i WHERE initial_income_data.statistic = i.type;
ALTER TABLE initial_income_data DROP COLUMN statistic;
ALTER TABLE initial_income_data ADD COLUMN idcounty bigint not null DEFAULT 0;
UPDATE initial_income_data SET idcounty = c.idcounty FROM county c WHERE c.county = initial_income_data.county_region;


ALTER TABLE initial_income_data DROP COLUMN county_region;


ALTER TABLE income_type ADD COLUMN unit text;

UPDATE income_type SET unit = i.unit FROM initial_income_data i WHERE i.idtype = income_type.idtype;

ALTER TABLE initial_income_data DROP COLUMN unit;

INSERT INTO sex(sex) SELECT DISTINCT sex FROM transformed_population_data;


ALTER TABLE transformed_population_data ADD COLUMN idsex bigint;

UPDATE transformed_population_data SET idsex = s.idsex FROM sex s WHERE transformed_population_data.sex = s.sex;

ALTER TABLE transformed_population_data DROP COLUMN sex;


CREATE TABLE crime AS SELECT idtype, id_station as idstation, year, count FROM transformed_crime_data;
CREATE TABLE population  AS SELECT idcounty, idsex, year, count FROM transformed_population_data;
CREATE TABLE income AS SELECT idcounty, idtype, year, value as count FROM initial_income_Data;


DROP TABLE transformed_crime_data;
DROP TABLE transformed_population_data;
DROP TABLE initial_income_data;

ALTER TABLE region ADD PRIMARY KEY(idregion);
ALTER TABLE region ALTER COLUMN idregion SET not null;
ALTER TABLE region ALTER COLUMN region SET not null;


ALTER TABLE authority ADD PRIMARY KEY(idauth);
ALTER TABLE authority ADD FOREIGN KEY (idregion) REFERENCES region;
ALTER TABLE authority ALTER COLUMN name SET not null;
ALTER TABLE authority ALTER COLUMN idregion SET not null;


ALTER TABLE county ADD PRIMARY KEY(idcounty);
ALTER TABLE county ADD FOREIGN KEY (idauth) REFERENCES authority;
ALTER TABLE county ALTER COLUMN county SET not null;
ALTER TABLE county  ALTER COLUMN area SET not null;
ALTER TABLE county ALTER COLUMN density SET not null;
ALTER TABLE county ALTER COLUMN province SET not null;
ALTER TABLE county ALTER COLUMN idauth SET not null;


ALTER TABLE sex add primary key(idsex);
ALTER TABLE sex ALTER COLUMN sex SET not null;

ALTER TABLE crime_type add primary key(idtype);
ALTER TABLE crime_type ALTER COLUMN type SET NOT NULL;

ALTER TABLE income_type ADD PRIMARY KEY(idtype);
ALTER TABLE income_type ALTER COLUMN type SET NOT NULL;
ALTER TABLE income_type ALTER COLUMN unit SET NOT NULL;



ALTER TABLE garda_station ADD PRIMARY KEY(idstation);
ALTER TABLE garda_station ADD FOREIGN KEY (idcounty) REFERENCES county;
ALTER TABLE garda_station ALTER COLUMN idcounty SET NOT NULL;
ALTER TABLE garda_station ALTER COLUMN idstation SET NOT NULL;
ALTER TABLE garda_station ALTER COLUMN station SET NOT NULL;

ALTER TABLE income ADD FOREIGN KEY (idcounty) REFERENCES county;
ALTER TABLE income ADD FOREIGN KEY (idtype) REFERENCES income_type;
ALTER TABLE income ADD UNIQUE(idcounty, idtype, year);
ALTER TABLE income ALTER COLUMN count SET not null;
ALTER TABLE income ALTER COLUMN idcounty SET not null;
ALTER TABLE income ALTER COLUMN idtype SET not null;
ALTER TABLE income ALTER COLUMN year SET DEFAULT extract(year FROM now());


ALTER TABLE crime ADD FOREIGN KEY (idtype) REFERENCES crime_type;
ALTER TABLE crime ADD FOREIGN KEY (idstation) REFERENCES garda_station;
ALTER TABLE crime ADD UNIQUE (idtype, idstation, year);
ALTER TABLE crime ALTER COLUMN idtype SET not null;
ALTER TABLE crime ALTER COLUMN idstation SET not null;
ALTER TABLE crime ALTER COLUMN count SET not null;
ALTER TABLE crime ALTER COLUMN year SET DEFAULT extract(year FROM now());


ALTER TABLE population add FOREIGN KEY (idcounty) REFERENCES county;
ALTER TABLE population add FOREIGN KEY (idsex) REFERENCES sex;
ALTER TABLE population ADD UNIQUE(idcounty,idsex,year);
ALTER TABLE population ALTER COLUMN idcounty SET not null;
ALTER TABLE population ALTER COLUMN idsex SET not null;
ALTER TABLE population ALTER COLUMN count SET not null;
ALTER TABLE population ALTER COLUMN year SET DEFAULT extract(year FROM now());

