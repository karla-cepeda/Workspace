DELIMITER $$
CREATE DEFINER=`tanniest_mybikes`@`%` PROCEDURE `BikesLastGPS`(curr varchar(10))
BEGIN

	SELECT gCurr.LastGPSTime, gCurr.BikeID, gCurr.Longitude, gCurr.Latitude, gCurr.InDublinArea, gCurr.InMobyArea, gCurr.Located, hb.Battery, hb.EBikeStateID, s.name, s.id as batteryid, hb.HarvestTime, EBS.name as nameebs

	FROM (select max(LastGPSTime) AS LastGPSTime, bikeID FROM gpsbikes GROUP BY bikeid) AS gMax
	INNER JOIN gpsbikes AS gCurr ON gCurr.LastGPSTime = gMax.LastGPSTime AND gCurr.bikeID = gMax.bikeID

	INNER JOIN (select max(HarvestTime) AS HarvestTime, bikeID FROM harvestedbikes GROUP BY bikeid) AS SmMax ON SmMax.bikeID = gCurr.bikeID
	INNER JOIN harvestedbikes AS hb ON hb.HarvestTime = SmMax.HarvestTime AND hb.bikeID = SmMax.bikeID

	INNER JOIN battery_status s on hb.Battery<=s.max and hb.Battery >=s.min
    INNER JOIN EBikeState EBS ON EBS.id = hb.EBikeStateID

	WHERE gCurr.Located = 1
	AND CAST(gCurr.LastGPSTime AS DATE) = STR_TO_DATE(curr, '%d/%m/%Y')


	UNION

	SELECT gLast.LastGPSTime, hb.BikeID, gLast.Longitude, gLast.Latitude, gCurr.InDublinArea, gCurr.InMobyArea, gCurr.Located, hb.Battery, hb.EBikeStateID, s.name, s.id as batteryid, hb.HarvestTime, EBS.name as nameebs

	FROM  (select max(HarvestTime) AS HarvestTime, bikeID FROM harvestedbikes WHERE CAST(HarvestTime AS DATE)  = STR_TO_DATE(curr, '%d/%m/%Y') GROUP BY bikeid) AS SmMax 
	INNER JOIN harvestedbikes AS hb ON hb.HarvestTime = SmMax.HarvestTime AND hb.bikeID = SmMax.bikeID

	INNER JOIN battery_status s on hb.Battery<=s.max and hb.Battery >=s.min
    INNER JOIN EBikeState EBS ON EBS.id = hb.EBikeStateID

	LEFT JOIN (select max(LastGPSTime) AS LastGPSTime, bikeID FROM gpsbikes WHERE CAST(LastGPSTime AS DATE)  = STR_TO_DATE(curr, '%d/%m/%Y') GROUP BY bikeid) AS gMax ON gMax.bikeID = hb.bikeID
	LEFT JOIN gpsbikes AS gCurr ON gCurr.LastGPSTime = gMax.LastGPSTime AND gCurr.bikeID = gMax.bikeID
	LEFT JOIN gpsbikes_lastvalid AS gLast ON hb.BikeID = gLast.BikeID

	WHERE 
	IFNULL(gCurr.Located,0) = 0

	ORDER BY BikeID;

END$$
DELIMITER ;
DELIMITER $$
CREATE DEFINER=`tanniest_mybikes`@`%` PROCEDURE `BikesRented`(curr varchar(10))
BEGIN


	SET @today =  STR_TO_DATE(curr, '%d/%m/%Y');

	select 
	LastRentalStart,
	BikeID
	from rentedbikes r
	where cast(LastRentalStart as date) = @today
	ORDER BY LastRentalStart;
    
END$$
DELIMITER ;
DELIMITER $$
CREATE DEFINER=`tanniest_mybikes`@`%` PROCEDURE `BikesRented_cum`(curr varchar(10))
BEGIN

	SELECT LastRentalStart, Total 
    FROM tanniest_mybikes.rentedbikes_daily_cumulative
    WHERE CAST(LastRentalStart AS DATE)  = STR_TO_DATE(curr, '%d/%m/%Y');

END$$
DELIMITER ;
DELIMITER $$
CREATE DEFINER=`tanniest_mybikes`@`%` PROCEDURE `BikesRented_perYear`(IN YEAR INT)
BEGIN
	SELECT COUNT(BikeID) AS Count, BikeID, MAX(LastRentalStart) AS LastDateRented FROM rentedbikes 
	WHERE YEAR(LastRentalStart) = YEAR OR YEAR = 0
	GROUP BY BikeID;
    
END$$
DELIMITER ;
DELIMITER $$
CREATE DEFINER=`tanniest_mybikes`@`%` PROCEDURE `get_batteryStatus`(curr varchar(10))
BEGIN
	SELECT 
	e.id,
	e.name,
	IFNULL(s.TOTAL,0) AS total
	FROM battery_status e
	LEFT JOIN (
		SELECT SUM(1) AS TOTAL, s.id
		FROM tanniest_mybikes.harvestedbikes h 
		INNER JOIN (select max(HarvestTime) AS HarvestTime, bikeID FROM harvestedbikes GROUP BY bikeid) AS SmMax ON h.bikeID = SmMax.bikeID and h.HarvestTime = SmMax.HarvestTime 
		INNER JOIN tanniest_mybikes.battery_status s on h.Battery<=s.max and h.Battery >=s.min
		WHERE CAST(h.HarvestTime AS DATE) = STR_TO_DATE(curr, '%d/%m/%Y')
		GROUP BY id
	) s 
	ON e.id = s.id;
END$$
DELIMITER ;
DELIMITER $$
CREATE DEFINER=`tanniest_mybikes`@`%` PROCEDURE `get_batterystatusbikes`(curr varchar(10))
BEGIN

	SELECT s.id, s.name, s.max, s.min, h.bikeid, h.battery, h.ebikestateid, eb.name
	FROM tanniest_mybikes.harvestedbikes h 
	INNER JOIN (select max(HarvestTime) AS HarvestTime, bikeID FROM harvestedbikes GROUP BY bikeid) AS SmMax ON h.bikeID = SmMax.bikeID and h.HarvestTime = SmMax.HarvestTime 
	INNER JOIN tanniest_mybikes.battery_status s on h.Battery<=s.max and h.Battery >=s.min
	inner join EBikeState eb on eb.id = h.EBikeStateID
	WHERE CAST(h.HarvestTime AS DATE) = STR_TO_DATE(curr, '%d/%m/%Y');

END$$
DELIMITER ;
DELIMITER $$
CREATE DEFINER=`tanniest_mybikes`@`%` PROCEDURE `get_batterystatusbikes_all`(curr varchar(10))
BEGIN

	SELECT h.bikeid, h.HarvestTime, s.id, s.name, s.max, s.min, h.bikeid, h.battery, h.ebikestateid, eb.name
	FROM tanniest_mybikes.harvestedbikes h 
	INNER JOIN tanniest_mybikes.battery_status s on h.Battery<=s.max and h.Battery >=s.min
	inner join EBikeState eb on eb.id = h.EBikeStateID
	WHERE CAST(h.HarvestTime AS DATE) = STR_TO_DATE(curr, '%d/%m/%Y');


END$$
DELIMITER ;
DELIMITER $$
CREATE DEFINER=`tanniest_mybikes`@`%` PROCEDURE `get_bikestatus`(curr varchar(10))
BEGIN

	SELECT 
	e.id,
	e.name,
	IFNULL(s.TOTAL,0) AS total
	FROM EBikeState e
	LEFT JOIN (
		SELECT COUNT(h.BikeId) AS TOTAL, h.EBikeStateID 
		FROM tanniest_mybikes.harvestedbikes h 
		INNER JOIN
		(select max(HarvestTime) AS HarvestTime, bikeID FROM harvestedbikes GROUP BY bikeid) AS SmMax ON h.bikeID = SmMax.bikeID and h.HarvestTime = SmMax.HarvestTime 
		WHERE CAST(h.HarvestTime AS DATE) = STR_TO_DATE(curr, '%d/%m/%Y')
		GROUP BY EBikeStateID
    ) s 
	ON e.id = s.EBikeStateID;

END$$
DELIMITER ;
DELIMITER $$
CREATE DEFINER=`tanniest_mybikes`@`%` PROCEDURE `get_cat_statusbattery`()
BEGIN

	SELECT * FROM battery_status;

END$$
DELIMITER ;
DELIMITER $$
CREATE DEFINER=`tanniest_mybikes`@`%` PROCEDURE `get_cat_statusbikes`()
BEGIN

	SELECT * FROM EBikeState;

END$$
DELIMITER ;
DELIMITER $$
CREATE DEFINER=`tanniest_mybikes`@`%` PROCEDURE `get_inarea`(curr varchar(10))
BEGIN

	SELECT 'In Area' AS label, count(1) AS total

	FROM  (select max(HarvestTime) AS HarvestTime, bikeID FROM harvestedbikes WHERE CAST(HarvestTime AS DATE) = STR_TO_DATE(curr, '%d/%m/%Y') GROUP BY bikeid) AS SmMax 
	INNER JOIN harvestedbikes AS hb ON hb.HarvestTime = SmMax.HarvestTime AND hb.bikeID = SmMax.bikeID

	LEFT JOIN (select max(LastGPSTime) AS LastGPSTime, bikeID FROM gpsbikes WHERE CAST(LastGPSTime AS DATE) = STR_TO_DATE(curr, '%d/%m/%Y') GROUP BY bikeid) AS gMax ON gMax.bikeID = hb.bikeID
	LEFT JOIN gpsbikes AS gCurr ON gCurr.LastGPSTime = gMax.LastGPSTime AND gCurr.bikeID = gMax.bikeID

	WHERE 
	IFNULL(gCurr.InMobyArea,False) = True and
    IFNULL(gCurr.Located,0) = 1


	UNION


	SELECT 'Out' AS label, count(1) AS total

	FROM  (select max(HarvestTime) AS HarvestTime, bikeID FROM harvestedbikes WHERE CAST(HarvestTime AS DATE) = STR_TO_DATE(curr, '%d/%m/%Y') GROUP BY bikeid) AS SmMax 
	INNER JOIN harvestedbikes AS hb ON hb.HarvestTime = SmMax.HarvestTime AND hb.bikeID = SmMax.bikeID

	LEFT JOIN (select max(LastGPSTime) AS LastGPSTime, bikeID FROM gpsbikes WHERE CAST(LastGPSTime AS DATE) = STR_TO_DATE(curr, '%d/%m/%Y') GROUP BY bikeid) AS gMax ON gMax.bikeID = hb.bikeID
	LEFT JOIN gpsbikes AS gCurr ON gCurr.LastGPSTime = gMax.LastGPSTime AND gCurr.bikeID = gMax.bikeID

	WHERE 
	IFNULL(gCurr.InMobyArea,True) = False and
    IFNULL(gCurr.Located,0) = 1
        


	UNION

	SELECT 'Unknown' AS label, count(1) AS total

	FROM  (select max(HarvestTime) AS HarvestTime, bikeID FROM harvestedbikes WHERE CAST(HarvestTime AS DATE)  = STR_TO_DATE(curr, '%d/%m/%Y') GROUP BY bikeid) AS SmMax 
	INNER JOIN harvestedbikes AS hb ON hb.HarvestTime = SmMax.HarvestTime AND hb.bikeID = SmMax.bikeID

	LEFT JOIN (select max(LastGPSTime) AS LastGPSTime, bikeID FROM gpsbikes WHERE CAST(LastGPSTime AS DATE)  = STR_TO_DATE(curr, '%d/%m/%Y') GROUP BY bikeid) AS gMax ON gMax.bikeID = hb.bikeID
	LEFT JOIN gpsbikes AS gCurr ON gCurr.LastGPSTime = gMax.LastGPSTime AND gCurr.bikeID = gMax.bikeID

	WHERE
    IFNULL(gCurr.Located,0) = 0;
    
END$$
DELIMITER ;
DELIMITER $$
CREATE DEFINER=`tanniest_mybikes`@`%` PROCEDURE `get_location`(curr varchar(10))
BEGIN
	SELECT 'Located' AS label, count(1) AS total

	FROM  (select max(HarvestTime) AS HarvestTime, bikeID FROM harvestedbikes WHERE CAST(HarvestTime AS DATE)  = STR_TO_DATE(curr, '%d/%m/%Y') GROUP BY bikeid) AS SmMax 
	INNER JOIN harvestedbikes AS hb ON hb.HarvestTime = SmMax.HarvestTime AND hb.bikeID = SmMax.bikeID


	LEFT JOIN (select max(LastGPSTime) AS LastGPSTime, bikeID FROM gpsbikes WHERE CAST(LastGPSTime AS DATE)  = STR_TO_DATE(curr, '%d/%m/%Y') GROUP BY bikeid) AS gMax ON gMax.bikeID = hb.bikeID
	LEFT JOIN gpsbikes AS gCurr ON gCurr.LastGPSTime = gMax.LastGPSTime AND gCurr.bikeID = gMax.bikeID

	WHERE 
	IFNULL(gCurr.Located,0) = 1


	UNION

	SELECT 'No Located' AS label, count(1) AS total

	FROM  (select max(HarvestTime) AS HarvestTime, bikeID FROM harvestedbikes WHERE CAST(HarvestTime AS DATE)  = STR_TO_DATE(curr, '%d/%m/%Y') GROUP BY bikeid) AS SmMax 
	INNER JOIN harvestedbikes AS hb ON hb.HarvestTime = SmMax.HarvestTime AND hb.bikeID = SmMax.bikeID


	LEFT JOIN (select max(LastGPSTime) AS LastGPSTime, bikeID FROM gpsbikes WHERE CAST(LastGPSTime AS DATE)  = STR_TO_DATE(curr, '%d/%m/%Y') GROUP BY bikeid) AS gMax ON gMax.bikeID = hb.bikeID
	LEFT JOIN gpsbikes AS gCurr ON gCurr.LastGPSTime = gMax.LastGPSTime AND gCurr.bikeID = gMax.bikeID

	WHERE 
	IFNULL(gCurr.Located,0) = 0;
    
END$$
DELIMITER ;
DELIMITER $$
CREATE DEFINER=`tanniest_mybikes`@`%` PROCEDURE `get_totalbikesrented`(curr varchar(10))
BEGIN

	select sum(case when r.bikeid is not null then 1 else 0 end) as total, b.bikeid, r.LastRentalStart as lasttimerented

	from bikes b
	left join 

	(
	select LastRentalStart, b1.bikeid 
	from rentedbikes b1
	inner join (select max(LastRentalStart) as date, bikeid from rentedbikes
					where cast(lastrentalstart as date)  = STR_TO_DATE(curr, '%d/%m/%Y') group by bikeid) bmax on bmax.bikeid = b1.bikeid
	where cast(lastrentalstart as date)  = STR_TO_DATE(curr, '%d/%m/%Y')
	) r on b.bikeid = r.bikeid 
	 
	group by b.bikeid
	order by total desc, b.bikeid desc;
    
END$$
DELIMITER ;
DELIMITER $$
CREATE DEFINER=`tanniest_mybikes`@`%` PROCEDURE `insert_cumrents`(curr varchar(10), currtime varchar(8))
BEGIN

	DECLARE total_rents BIGINT(20);
    DECLARE datetimerental datetime;
    
    SET total_rents = (SELECT COUNT(1) 
						FROM rentedbikes 
						WHERE CAST(LastRentalStart AS DATE) = STR_TO_DATE(curr, '%d/%m/%Y'));
                        
	SET datetimerental = STR_TO_DATE(CONCAT(curr,' ',currtime), '%d/%m/%Y %H:%i:%s');
                            
	INSERT INTO rentedbikes_daily_cumulative(LastRentalStart, Total) VALUES (datetimerental, total_rents);
    
    #SELECT total_rents, datetimerental, curr, currtime, STR_TO_DATE(curr, '%d/%m/%Y') AS DATEFTO;
	
END$$
DELIMITER ;
DELIMITER $$
CREATE DEFINER=`tanniest_mybikes`@`%` PROCEDURE `lastinfo`(curr varchar(10))
BEGIN
	SELECT harvestTime, 
	BikeID,
	hour(HarvestTime) as by_hour, 
	battery, 

	CASE 
	WHEN EBikeStateID = 1 THEN 'Warning - is in move and not rented'
	WHEN EBikeStateID = 2 THEN 'Normal'
	WHEN EBikeStateID = 3 THEN 'Switched Off'
	WHEN EBikeStateID = 4 THEN 'Firmware Upgrade'
	WHEN EBikeStateID = 5 THEN 'Laying on the ground' END AS EBikeState,
	EBikeStateID,
	CASE 
	WHEN battery BETWEEN 61 AND 100 THEN 'PERFECT'
	WHEN battery BETWEEN 21 AND 60 THEN 'GOOD'
	WHEN battery BETWEEN 1 AND 20 THEN 'WARNING'
	ELSE 'DEAD' END AS battery_status,

	CASE 
	WHEN battery BETWEEN 61 AND 100 THEN 0
	WHEN battery BETWEEN 21 AND 60 THEN 1
	WHEN battery BETWEEN 1 AND 20 THEN 2
	ELSE 3 END AS battery_status_id

	FROM tanniest_mybikes.harvestedbikes
	WHERE CAST(HarvestTime AS DATE) = STR_TO_DATE(curr, '%d/%m/%Y')
	order by HarvestTime;
END$$
DELIMITER ;
DELIMITER $$
CREATE DEFINER=`tanniest_mybikes`@`%` PROCEDURE `summary`(curr varchar(10))
BEGIN

	SELECT 'Total bikes' AS label, count(1) AS total FROM bikes b
	UNION

	SELECT 'In the street', count(1) FROM bikes b
	INNER JOIN (select max(HarvestTime) AS HarvestTime, bikeID FROM harvestedbikes WHERE CAST(HarvestTime AS DATE)  = STR_TO_DATE(curr, '%d/%m/%Y') GROUP BY bikeid) AS SmMax ON SmMax.bikeID = b.bikeID

	UNION

	select 'Total rentals', COUNT(1) from rentedbikes r where cast(LastRentalStart as date)  = STR_TO_DATE(curr, '%d/%m/%Y')

	UNION

	SELECT 'Bikes no located', COUNT(1)

	FROM  (select max(HarvestTime) AS HarvestTime, bikeID FROM harvestedbikes WHERE CAST(HarvestTime AS DATE)  = STR_TO_DATE(curr, '%d/%m/%Y') GROUP BY bikeid) AS SmMax 
	INNER JOIN harvestedbikes AS hb ON hb.HarvestTime = SmMax.HarvestTime AND hb.bikeID = SmMax.bikeID


	LEFT JOIN (select max(LastGPSTime) AS LastGPSTime, bikeID FROM gpsbikes WHERE CAST(LastGPSTime AS DATE)  = STR_TO_DATE(curr, '%d/%m/%Y') GROUP BY bikeid) AS gMax ON gMax.bikeID = hb.bikeID
	LEFT JOIN gpsbikes AS gCurr ON gCurr.LastGPSTime = gMax.LastGPSTime AND gCurr.bikeID = gMax.bikeID
	LEFT JOIN gpsbikes_lastvalid AS gLast ON gCurr.BikeID = gLast.BikeID

	WHERE 
	IFNULL(gCurr.Located,0) = 0
    

	UNION

	SELECT 'Bikes off', COUNT(1)
	FROM (select max(HarvestTime) AS HarvestTime, bikeID FROM harvestedbikes GROUP BY bikeid) AS SmMax
	INNER JOIN harvestedbikes AS hb ON hb.HarvestTime = SmMax.HarvestTime AND hb.bikeID = SmMax.bikeID
	WHERE IFNULL(hb.Battery, 0) = 0
	AND CAST(hb.HarvestTime AS DATE)  = STR_TO_DATE(curr, '%d/%m/%Y')

	;


END$$
DELIMITER ;
