-- stored procedure
-- The moving average is computed just for open_price variable, as it is
--    the variable of interest selected from time series analysis.
--    20, 50 and 200 periods were selected as they are significant to spot perfect oportunities to buy
--    or mark the time to sell.
create or replace function public.get_ma_20_50_200(symbol INTEGER)
  returns table(
	symbol_id INTEGER,
	symbol_name TEXT,
  	id INTEGER,
	date DATE,
	open_price NUMERIC,
	moving_average20 NUMERIC,
	moving_average50 NUMERIC,
	moving_average200 NUMERIC	  
  ) as
$Body$
	WITH prices_ma AS (
		SELECT
		id,
		symbol_id,
		date_price,
		open_price,
		AVG(open_price) OVER ma20  AS moving_average20,
		AVG(open_price) OVER ma50  AS moving_average50,
		AVG(open_price) OVER ma200 AS moving_average200,
		ROW_NUMBER() OVER(ORDER BY date_price) AS date_flag
		FROM public.daily_data
		WHERE symbol_id = symbol
		WINDOW
		ma20  AS (PARTITION BY symbol_id ORDER BY date_price ASC ROWS BETWEEN 20 PRECEDING AND CURRENT ROW),
		ma50  AS (PARTITION BY symbol_id ORDER BY date_price ASC ROWS BETWEEN 50 PRECEDING AND CURRENT ROW),
		ma200 AS (PARTITION BY symbol_id ORDER BY date_price ASC ROWS BETWEEN 200 PRECEDING AND CURRENT ROW)
		
	)
	SELECT
	d1.symbol_id, 
	sy1.ticker AS symbol_name,
	d1.id, 
	d1.date_price, 
	d1.open_price,
	CASE 
		WHEN (d1.date_flag < 20) THEN NULL
		ELSE TRUNC(d1.moving_average20, 4) 
	END AS moving_average20,	
	CASE 
		WHEN (d1.date_flag < 50) THEN NULL
		ELSE TRUNC(d1.moving_average20, 4) 
	END AS moving_average50,	
	CASE 
		WHEN (d1.date_flag < 200) THEN NULL
		ELSE TRUNC(d1.moving_average200, 4) 
	END AS moving_average200
	
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
	moving_average20,
	moving_average50,
	moving_average200
FROM get_ma_20_50_200(1);