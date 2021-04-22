-- Downsample time series object to a weekly grain
create or replace function public.get_weekly_downsampling(symbol INTEGER, max_date DATE DEFAULT NOW(), min_date DATE DEFAULT NOW()) 
  returns table(
	  year INTEGER,
	  month INTEGER,
	  week INTEGER,
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
	DATE_PART('week' , d1.date_price) AS "week",	
	TRUNC(AVG(d1.open_price),  2) AS open_price,
	TRUNC(AVG(d1.high_price),  2) AS high_price,
	TRUNC(AVG(d1.low_price),   2) AS low_price,
	TRUNC(AVG(d1.close_price), 2) AS close_price,
	SUM(d1.volume) AS volume
	FROM public.daily_data d1
	WHERE d1.symbol_id = symbol 
	AND CAST(d1.date_price AS DATE) BETWEEN CAST(max_date AS DATE) AND CAST(min_date AS DATE)
	GROUP BY 
	DATE_PART('week', d1.date_price),
	DATE_PART('month', d1.date_price),
	DATE_PART('year', d1.date_price),
	d1.symbol_id
	ORDER BY "year", "week" ASC;
		
$Body$
language sql;

SELECT * FROM get_weekly_downsampling(1, '2021-01-01');