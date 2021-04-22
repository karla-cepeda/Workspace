-- #import all data to tables
\copy initial_income_data FROM 'income.csv' CSV HEADER;
\copy initial_population_data FROM 'population.csv' CSV HEADER;
\copy initial_crime_data FROM 'crime.csv' CSV HEADER;
