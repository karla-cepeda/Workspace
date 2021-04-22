DROP TABLE IF EXISTS transformed_crime_data;
CREATE TABLE transformed_crime_data(
statistic TEXT NOT NULL,
type_offence TEXT NOT NULL,
unit TEXT NOT NULL,
year bigint NOT NULL,
count BIGINT NOT NULL DEFAULT 0,
id_station bigint not null,
station_division text not null,
station text not null
);

DROP TABLE IF EXISTS transformed_population_data;
CREATE TABLE transformed_population_data(
statistic TEXT NOT NULL,
county TEXT NOT NULL,
sex TEXT NOT NULL,
unit TEXT NOT NULL,
year bigint NOT NULL,
count BIGINT NOT NULL DEFAULT 0
);

