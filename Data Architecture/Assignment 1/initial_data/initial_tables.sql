DROP TABLE IF EXISTS initial_crime_data;
CREATE TABLE initial_crime_data(
statistic TEXT NOT NULL,
garda_station TEXT NOT NULL,
type_offence TEXT NOT NULL,
unit TEXT NOT NULL,
y2003 BIGINT NOT NULL DEFAULT 0,
y2004 BIGINT NOT NULL DEFAULT 0,
y2005 BIGINT NOT NULL DEFAULT 0,
y2006 BIGINT NOT NULL DEFAULT 0,
y2007 BIGINT NOT NULL DEFAULT 0,
y2008 BIGINT NOT NULL DEFAULT 0,
y2009 BIGINT NOT NULL DEFAULT 0,
y2010 BIGINT NOT NULL DEFAULT 0,
y2011 BIGINT NOT NULL DEFAULT 0,
y2012 BIGINT NOT NULL DEFAULT 0,
y2013 BIGINT NOT NULL DEFAULT 0,
y2014 BIGINT NOT NULL DEFAULT 0,
y2015 BIGINT NOT NULL DEFAULT 0,
y2016 BIGINT NOT NULL DEFAULT 0,
y2017 BIGINT NOT NULL DEFAULT 0,
y2018 BIGINT NOT NULL DEFAULT 0,
y2019 BIGINT NOT NULL DEFAULT 0
);

DROP TABLE IF EXISTS initial_population_data;
CREATE TABLE initial_population_data(
statistic TEXT NOT NULL,
county TEXT NOT NULL,
sex TEXT NOT NULL,
unit TEXT NOT NULL,
y1841 BIGINT NOT NULL DEFAULT 0,
y1851 BIGINT NOT NULL DEFAULT 0,
y1861 BIGINT NOT NULL DEFAULT 0,
y1871 BIGINT NOT NULL DEFAULT 0,
y1881 BIGINT NOT NULL DEFAULT 0,
y1891 BIGINT NOT NULL DEFAULT 0,
y1901 BIGINT NOT NULL DEFAULT 0,
y1911 BIGINT NOT NULL DEFAULT 0,
y1926 BIGINT NOT NULL DEFAULT 0,
y1936 BIGINT NOT NULL DEFAULT 0,
y1946 BIGINT NOT NULL DEFAULT 0,
y1951 BIGINT NOT NULL DEFAULT 0,
y1956 BIGINT NOT NULL DEFAULT 0,
y1961 BIGINT NOT NULL DEFAULT 0,
y1966 BIGINT NOT NULL DEFAULT 0,
y1971 BIGINt NOT NULL DEFAULT 0,
y1979 BIGINT NOT NULL DEFAULT 0,
y1981 BIGINT NOT NULL DEFAULT 0,
y1986 BIGINT NOT NULL DEFAULT 0,
y1991 BIGINT NOT NULL DEFAULT 0,
y1996 BIGINT NOT NULL DEFAULT 0,
y2002 BIGINT NOT NULL DEFAULT 0,
y2006 BIGINT NOT NULL DEFAULT 0,
y2011 BIGINT NOT NULL DEFAULT 0,
y2016 BIGINT NOT NULL DEFAULT 0
);

DROP TABLE IF EXISTS initial_income_data;
CREATE TABLE initial_income_data(
statistic TEXT NOT NULL,
year bigint NOT NULL DEFAULT 0,
county_region TEXT NOT NULL,
unit TEXT NOT NULL,
value money NOT NULL DEFAULT 0
);
