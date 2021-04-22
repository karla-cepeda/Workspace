SELECT ci.id AS city_id, ci.name AS city_name, s.id AS state_id, s.name AS state_name, co.id AS country_id, co.name AS country_name, ti.id AS timezone_id, ti.name AS timezone_name 
FROM public.city ci INNER JOIN public.timezones ti ON ci.timezone_id = ti.id 
INNER JOIN public.county cou ON ci.county_id = cou.id 
INNER JOIN public.state s ON cou.state_id = s.id 
INNER JOIN public.country co ON s.country_id = co.id 
WHERE LOWER(ci.name) = %s AND LOWER(s.abbrev) = %s

