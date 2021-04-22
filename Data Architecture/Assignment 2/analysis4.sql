-- Downsample time series object to a weekly grain
create or replace function public.get_monthly_downsampling(symbol INTEGER, max_date DATE DEFAULT NOW(), min_date DATE DEFAULT NOW()) 
  returns table(
	  year INTEGER,
	  month INTEGER,
	  open_price NUMERIC,
	  high_price NUMERIC,
	  low_price NUMERIC,
	  close_price NUMERIC,
	  volume NUMERIC
  ) AS
$Body$
	SELECT 
	DATE_PART('year' , d1.date_price) AS "year",
	DATE_PART('month', d1.date_price) AS "month",	
	TRUNC(AVG(d1.open_price),  2) AS open_price,
	TRUNC(AVG(d1.high_price),  2) AS high_price,
	TRUNC(AVG(d1.low_price),   2) AS low_price,
	TRUNC(AVG(d1.close_price), 2) AS close_price,
	SUM(d1.volume) AS volume
	FROM public.daily_data d1
	WHERE d1.symbol_id = symbol 
	AND CAST(d1.date_price AS DATE) BETWEEN CAST(max_date AS DATE) AND CAST(min_date AS DATE)
	GROUP BY 
	DATE_PART('month', d1.date_price),
	DATE_PART('year', d1.date_price),
	d1.symbol_id
	ORDER BY "year", "month" ASC;
		
$Body$
language sql;

-- example
-- In 2020, March was the worst month of the year for PayPal stock. The stock price dropped below 100
--   It makes sense as the mareket experience a major crash between Febraruy and March.
--   The volume (number of times people buy/sell) in this month has the highest number.
SELECT 
year, 
month, 
open_price,
volume
FROM get_monthly_downsampling(1, '2020-01-01', '2020-12-31')
ORDER BY open_price ASC;