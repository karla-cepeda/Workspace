CREATE TABLE `battery_status` (
  `id` int(11) NOT NULL,
  `name` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `max` int(11) NOT NULL,
  `min` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
INSERT INTO `tanniest_mybikes`.`battery_status`(`id`,`name`,`max`,`min`)VALUES(1,'Perfect',100,60);
INSERT INTO `tanniest_mybikes`.`battery_status`(`id`,`name`,`max`,`min`)VALUES(2,'Good',59,20);
INSERT INTO `tanniest_mybikes`.`battery_status`(`id`,`name`,`max`,`min`)VALUES(3,'Warning',19,1);
INSERT INTO `tanniest_mybikes`.`battery_status`(`id`,`name`,`max`,`min`)VALUES(4,'Dead',0,0);
CREATE TABLE `bikes` (
  `BikeID` bigint(20) DEFAULT NULL,
  `BikeIdentifier` bigint(20) DEFAULT NULL,
  `BikeTypeName` text COLLATE utf8_unicode_ci,
  `EBikeProfileID` bigint(20) DEFAULT NULL,
  `IsEBike` tinyint(1) DEFAULT NULL,
  `IsMotor` tinyint(1) DEFAULT NULL,
  `IsSmartLock` tinyint(1) DEFAULT NULL,
  `SpikeID` bigint(20) DEFAULT NULL,
  `active` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
CREATE TABLE `dublinmap` (
  `Id` bigint(20) DEFAULT NULL,
  `Longitude` double DEFAULT NULL,
  `Latitude` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
CREATE TABLE `EBikeState` (
  `id` int(11) NOT NULL,
  `name` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
INSERT INTO `tanniest_mybikes`.`EBikeState`(`id`,`name`)VALUES(1,'Warning! - Moving and not rented');
INSERT INTO `tanniest_mybikes`.`EBikeState`(`id`,`name`)VALUES(2,'Normal');
INSERT INTO `tanniest_mybikes`.`EBikeState`(`id`,`name`)VALUES(3,'Switched Off');
INSERT INTO `tanniest_mybikes`.`EBikeState`(`id`,`name`)VALUES(4,'Firmware Upgrade');
INSERT INTO `tanniest_mybikes`.`EBikeState`(`id`,`name`)VALUES(5,'Laying on the ground');
CREATE TABLE `gpsbikes` (
  `LastGPSTime` datetime DEFAULT NULL,
  `BikeID` bigint(20) DEFAULT NULL,
  `Latitude` double DEFAULT NULL,
  `Longitude` double DEFAULT NULL,
  `InDublinArea` tinyint(1) DEFAULT NULL,
  `InMobyArea` tinyint(1) DEFAULT NULL,
  `Located` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
CREATE TABLE `gpsbikes_lastvalid` (
  `LastGPSTime` datetime DEFAULT NULL,
  `BikeID` bigint(20) DEFAULT NULL,
  `Latitude` double DEFAULT NULL,
  `Longitude` double DEFAULT NULL,
  `InDublinArea` tinyint(1) DEFAULT NULL,
  `InMobyArea` tinyint(1) DEFAULT NULL,
  `Located` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
CREATE TABLE `harvestedbikes` (
  `HarvestTime` datetime DEFAULT NULL,
  `BikeID` bigint(20) DEFAULT NULL,
  `Battery` bigint(20) DEFAULT NULL,
  `EBikeStateID` bigint(20) DEFAULT NULL,
  KEY `HarvestTime` (`HarvestTime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `lastdatevisit` (
  `lastDateVisit` datetime NOT NULL,
  `description` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `mobyarea` (
  `Id` bigint(20) DEFAULT NULL,
  `Longitude` double DEFAULT NULL,
  `Latitude` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
CREATE TABLE `rentedbikes` (
  `LastRentalStart` datetime DEFAULT NULL,
  `BikeID` bigint(20) DEFAULT NULL,
  KEY `LastRentalStart_Sorted` (`LastRentalStart`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `rentedbikes_daily_cumulative` (
  `LastRentalStart` datetime NOT NULL,
  `Total` bigint(20) NOT NULL DEFAULT '0',
  PRIMARY KEY (`LastRentalStart`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
