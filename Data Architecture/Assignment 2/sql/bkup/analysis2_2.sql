create or replace function public.get_ma(symbol INTEGER, periods INTEGER DEFAULT 5, max_date DATE DEFAULT NOW(), min_date DATE DEFAULT NOW()) 
  returns table(
	symbol_id INTEGER,
	symbol_name TEXT,
  	id INTEGER,
	date DATE,
	open_price NUMERIC,
	moving_average NUMERIC
	  
  ) as
$Body$
	WITH prices_ma AS (
		SELECT
		id,
		symbol_id,
		date_price,
		open_price,
		AVG(open_price) OVER (PARTITION BY symbol_id ORDER BY date_price ASC ROWS BETWEEN periods PRECEDING AND CURRENT ROW) AS moving_average,
		ROW_NUMBER() OVER(ORDER BY date_price) AS date_flag
		FROM public.daily_data
		WHERE symbol_id = symbol
		AND date_price BETWEEN CAST(max_date AS DATE) AND CAST(min_date AS DATE)
	)
	SELECT
	d1.symbol_id, 
	sy1.ticker AS symbol_name,
	d1.id, 
	d1.date_price, 
	d1.open_price,
	CASE 
		WHEN (d1.date_flag < periods) THEN NULL
		ELSE TRUNC(d1.moving_average, 4) 
	END AS moving_average
	FROM prices_ma d1
	INNER JOIN symbol sy1 on sy1.id = d1.symbol_id
	
	ORDER BY d1.date_price
  
$Body$
language sql;

-- example
SELECT 
	symbol_name,
	date,
	open_price,
	moving_average
FROM get_ma(1, 10, '2021-01-01');
