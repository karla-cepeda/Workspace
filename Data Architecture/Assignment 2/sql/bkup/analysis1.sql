-- stored procedure
-- The percentage change is computed just for open_price variable, as it is
--    the variable of interest selected from time series analysis.
create or replace function public.get_pctchange(symbol INTEGER, max_date DATE DEFAULT NOW(), min_date DATE DEFAULT NOW()) 
  returns table(
  	id INTEGER,
	symbol_id INTEGER,
	symbol_name TEXT,
	date DATE,
	open_price NUMERIC,
	shift_price NUMERIC,
	pct_change NUMERIC,
	indicator_id INTEGER,
	indicator TEXT
  ) as
$Body$
	WITH prices AS (
		SELECT id,
		symbol_id, 
		date_price, 
		open_price, 
		LAG(open_price,1) OVER(PARTITION BY symbol_id ORDER BY date_price) AS lag_open_price 
		FROM public.daily_data 
		WHERE symbol_id = symbol
		AND date_price BETWEEN CAST(max_date AS DATE) AND CAST(min_date AS DATE)

	)
	SELECT d1.id, 
	d1.symbol_id, 
	sy1.ticker AS symbol_name,
	d1.date_price, 
	d1.open_price,
	d1.lag_open_price AS lag_open_price,
	TRUNC((d1.open_price - d1.lag_open_price)/d1.lag_open_price, 10) AS pct_change,
	CASE 
		WHEN d1.lag_open_price is NULL THEN NULL 
		WHEN d1.open_price > d1.lag_open_price THEN 1 
		WHEN d1.open_price < d1.lag_open_price THEN  0
		ELSE 3
	END AS indicator_id,
	CASE 
		WHEN d1.lag_open_price is NULL THEN NULL 
		WHEN d1.open_price > d1.lag_open_price THEN 'UP' 
		WHEN d1.open_price < d1.lag_open_price THEN 'DOWN'
		ELSE 'REMAIN'
	END AS Indicator

	FROM prices d1
	INNER JOIN symbol sy1 on sy1.id = d1.symbol_id	
	ORDER BY d1.date_price
  
$Body$
language sql;

-- example
SELECT 
	symbol_name,
	date,
	open_price,
	pct_change,
	indicator_id,
	indicator
FROM get_pctchange(1, '2021-01-01');