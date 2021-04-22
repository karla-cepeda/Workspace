
-- QUERIES TO ANSWER QUESTIONS

CREATE OR REPLACE VIEW crime_per_county_per_year AS 
SELECT co.idcounty, co.county, c.year, SUM(c.count) 
FROM crime c 
INNER JOIN garda_station s on s.idstation = c.idstation 
INNER JOIN county co on co.idcounty = s.idcounty group by co.county, c.year, co.idcounty 
ORDER BY co.county, c.year, co.idcounty;


CREATE OR REPLACE VIEW population_per_county_per_year AS 
SELECT co.idcounty, co.county, p.year, SUM(p.count) 
FROM population p 
INNER JOIN county co ON p.idcounty = co.idcounty 
GROUP BY co.county, p.year, co.idcounty ORDER BY co.county, p.year, co.idcounty;

CREATE OR REPLACE VIEW income_per_county_per_year AS 
SELECT co.idcounty, co.county, i.year, SUM(i.count) 
FROM income i 
INNER JOIN county co on i.idcounty = co.idcounty 
WHERE idtype = 9 group by co.county, i.year, co.idcounty 
ORDER BY co.county, i.year, co.idcounty;


CREATE OR REPLACE VIEW summary_per_county_per_year AS 
SELECT c.county, c.year, c.sum as recorded_crime_offences, i.sum AS total_household_income, p.sum AS total_population 
FROM crime_per_county_per_year c 
INNER JOIN income_per_county_per_year i on c.idcounty = i.idcounty and c.year = i.year 
INNER JOIN population_per_county_per_year p on c.idcounty = p.idcounty and c.year = p.year;


CREATE OR REPLACE VIEW summary_per_county AS 
SELECT c.county, ROUND(AVG(c.sum)) as recorded_crime_offences, CAST(AVG(CAST(i.sum as decimal(15,2))) as money) as total_household_income, ROUND(AVG(p.sum)) as total_population 
FROM crime_per_county_per_year c 
INNER JOIN income_per_county_per_year i ON c.idcounty = i.idcounty AND c.year = i.year 
INNER JOIN population_per_county_per_year p ON c.idcounty = p.idcounty and c.year = p.year 
GROUP BY c.county;

SELECT * FROM crime_per_county_per_year;
SELECT * FROM population_per_county_per_year;
SELECT * FROM income_per_county_per_year;
SELECT * FROM summary_per_county_per_year;
SELECT * FROM summary_per_county;

