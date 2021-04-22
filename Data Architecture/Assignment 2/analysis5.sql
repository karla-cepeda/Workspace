-- Total Volume of stocks buy/sell
-- PayPal Stock
SELECT
	d1.id,
	d1.symbol_id,
	sy1.ticker AS symbol_name,
	d1.date_price,
	d1.volume,
	SUM(d1.volume) OVER (
      	PARTITION BY d1.symbol_id
		ORDER BY d1.date_price ASC
      	RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
	) AS total_volumne
FROM public.daily_data d1
INNER JOIN public.symbol sy1 ON sy1.id = d1.symbol_id
WHERE
d1.symbol_id = 1
ORDER BY
d1.date_price;
