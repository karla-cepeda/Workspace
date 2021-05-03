use tanniest_mybikes;

select distinct h.*, g2.*
from harvestedbikes h

inner join (SELECT max(HarvestTime) as HarvestTime, bikeid 
			FROM harvestedbikes 
            group by bikeid) hmax on h.HarvestTime = hmax.HarvestTime and h.bikeid = hmax.bikeid
            
inner join (select max(LastGPSTime) as LastGPSTime, bikeID 
			from gpsbikes 
            group by bikeid) g on g.bikeid = h.bikeid and hmax.bikeid = g.bikeid
            
inner join gpsbikes g2 on g2.LastGPSTime = g.LastGPSTime and g.bikeID = g2.bikeID and hmax.bikeid = g2.bikeid

order by h.BikeId;
