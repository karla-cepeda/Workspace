create or replace function public.get_pctchange(symbol INTEGER, max_date DATE DEFAULT NOW(), min_date DATE DEFAULT NOW()) 
  returns table(
  	id INTEGER,
	symbol_id INTEGER,
	date DATE,
	open_price NUMERIC,
	pct_change NUMERIC,
	indicator_id INTEGER,
	indicator TEXT
  ) as
$Body$
	WITH prices AS (
		SELECT id, symbol_id, date_price, open_price, ROW_NUMBER() OVER(ORDER BY id) AS n FROM public.daily_data 
		WHERE symbol_id = symbol
		AND date_price BETWEEN CAST(max_date AS DATE) AND CAST(min_date AS DATE)
	), shift_prices AS (
		SELECT id, open_price, ROW_NUMBER() OVER(ORDER BY id) + 1 AS n FROM public.daily_data 
		WHERE symbol_id = symbol
		AND date_price BETWEEN CAST(max_date AS DATE) AND CAST(min_date AS DATE)
	)
	SELECT d1.id, 
	d1.symbol_id, 
	d1.date_price, 
	d1.open_price,
	TRUNC((d1.open_price - d2.open_price)/d2.open_price, 10) AS pct_change,
	CASE 
		WHEN d2.open_price is NULL THEN NULL 
		WHEN d1.open_price > d2.open_price THEN 1 
		WHEN d1.open_price < d2.open_price THEN  0
		ELSE 3
	END AS indicator_id,
	CASE 
		WHEN d2.open_price is NULL THEN NULL 
		WHEN d1.open_price > d2.open_price THEN 'INCREASE' 
		WHEN d1.open_price < d2.open_price THEN  'DECREASE'
		ELSE 'NO CHANGE'
	END AS Indicator

	FROM prices d1
	LEFT OUTER JOIN shift_prices d2 ON d1.n = d2.n
	
	ORDER BY d1.date_price
  
$Body$
language sql;

-- example
SELECT id,
	symbol_id,
	date,
	open_price,
	pct_change,
	indicator_id,
	indicator
FROM get_pctchange(1, '2021-01-01', '2021-02-01');