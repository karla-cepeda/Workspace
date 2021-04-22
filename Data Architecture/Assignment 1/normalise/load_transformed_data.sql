-- #import all data to tables
\copy transformed_population_data FROM 'population_2.csv' CSV HEADER;
\copy transformed_crime_data FROM 'crime_2.csv' CSV HEADER;
