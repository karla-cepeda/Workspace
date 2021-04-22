\o load_verification.txt;

SELECT nspname AS schemaname,relname AS tables ,reltuples AS rows
FROM pg_class C
LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)
WHERE 
  nspname NOT IN ('pg_catalog', 'information_schema') AND
  relkind='r' AND
  relname LIKE 'initial_%'
ORDER BY reltuples DESC;

\d initial_crime_data;
\d initial_population_data;
\d initial_income_data;

