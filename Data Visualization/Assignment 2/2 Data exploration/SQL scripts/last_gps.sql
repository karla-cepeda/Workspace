SELECT gCurr.* 
FROM (select max(LastGPSTime) AS LastGPSTime, bikeID FROM gpsbikes GROUP BY bikeid) AS gMax
INNER JOIN gpsbikes AS gCurr ON gCurr.LastGPSTime = gMax.LastGPSTime AND gCurr.bikeID = gMax.bikeID
WHERE gCurr.Located = True
UNION
SELECT gCurr.LastGPSTime, gCurr.BikeID, gLast.Longitude, gLast.Latitude, gCurr.InDublinArea, gCurr.InMobyArea, gCurr.Located 
FROM (select max(LastGPSTime) AS LastGPSTime, bikeID FROM gpsbikes GROUP BY bikeid) AS gMax
INNER JOIN gpsbikes AS gCurr ON gCurr.LastGPSTime = gMax.LastGPSTime AND gCurr.bikeID = gMax.bikeID
INNER JOIN gpsbikes_lastvalid AS gLast ON gCurr.BikeID = gLast.BikeID
WHERE gCurr.Located = False
ORDER BY BikeID;
