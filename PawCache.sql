-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: pawcache
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `animal_dat`
--

DROP TABLE IF EXISTS `animal_dat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `animal_dat` (
  `animal_id` int(5) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `name` varchar(15) DEFAULT NULL,
  `animal_type` varchar(15) DEFAULT NULL,
  `species` varchar(25) DEFAULT NULL,
  `block` char(3) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `brought_on` date DEFAULT NULL,
  `last_checkup` date DEFAULT NULL,
  `due_checkup` date DEFAULT NULL,
  `health_notes` varchar(128) DEFAULT NULL,
  `feeds_per_day` int DEFAULT NULL,
  `feed_type` varchar(25) DEFAULT NULL,
  `feeds_today` int DEFAULT NULL,
  `cage_cleaning` date DEFAULT NULL,
  PRIMARY KEY (`animal_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `animal_dat`
--

LOCK TABLES `animal_dat` WRITE;
/*!40000 ALTER TABLE `animal_dat` DISABLE KEYS */;
INSERT INTO `animal_dat` VALUES (00001,'roxy','Mammal','Red Panda','C02',0,'2024-12-15','2025-05-20','2025-06-15','Active and playful',2,'Fruits,Bamboo',1,'2025-06-30'),(00002,'Spike','Reptile','Iguana','D03',5,'2023-11-10','2025-05-26','2025-06-15','Needs more UV exposure',1,'Insects',1,'2025-06-10'),(00003,'Luna','Bird','Parrot','A01',2,'2023-03-12','2025-05-10','2025-06-10','Molting season started',2,'Seeds',2,'2025-06-12'),(00004,'Max','Mammal','Capybara','B05',4,'2024-02-28','2025-05-18','2025-06-18','Calm and social',3,'Vegetables',2,'2025-06-20'),(00005,'Zara','Reptile','Chameleon','D01',3,'2023-06-15','2025-05-22','2025-06-22','Needs humidity control',1,'Insects',1,'2025-06-11'),(00006,'Bruno','Mammal','Lemur','C04',6,'2022-12-01','2025-05-19','2025-06-19','Very active',2,'Fruits',2,'2025-06-25'),(00007,'Skye','Bird','Owl','A03',5,'2024-05-22','2025-05-24','2025-06-24','Nocturnal, needs quiet',1,'Rodents',1,'2025-06-14'),(00008,'Nala','Mammal','Meerkat','B02',2,'2023-09-05','2025-05-23','2025-06-23','Needs group interaction',2,'Insects',2,'2025-06-18'),(00009,'Khan','Mammal','Bengal Tiger','C05',4,'2023-08-12','2025-05-25','2025-06-25','Healthy and active',2,'Meat,Fish',1,'2025-07-05'),(00010,'Snowy','Mammal','Siberian Tiger','C05',3,'2023-08-12','2025-05-26','2025-06-26','Prefers cooler areas',2,'Meat',1,'2025-07-06'),(00011,'Leo','Mammal','Bengal Tiger','C06',5,'2023-08-12','2025-05-23','2025-06-23','Aggressive behavior noted',2,'Meat,Fish',1,'2025-07-07'),(00012,'Ice','Mammal','Siberian Tiger','C06',2,'2023-08-12','2025-05-27','2025-06-27','Adapting well',2,'Meat',1,'2025-07-08'),(00013,'Simba','Mammal','African Lion','C07',3,'2023-07-10','2025-05-24','2025-06-24','Very active',2,'Meat',1,'2025-07-09'),(00014,'Zuba','Mammal','Asian Lion','C07',4,'2022-09-15','2025-05-26','2025-06-26','Needs more space',2,'Meat',1,'2025-07-10'),(00015,'Mufasa','Mammal','African Lion','C08',6,'2021-05-05','2025-05-22','2025-06-22','Dominant and territorial',2,'Meat',1,'2025-07-11'),(00016,'Raj','Mammal','Asian Lion','C08',5,'2023-06-18','2025-05-25','2025-06-25','Observant and calm',2,'Meat',1,'2025-07-12');
/*!40000 ALTER TABLE `animal_dat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `food_dir`
--

DROP TABLE IF EXISTS `food_dir`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `food_dir` (
  `itemno` int(6) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `item` varchar(15) DEFAULT NULL,
  `in_stock` int DEFAULT NULL,
  `stock_unit` varchar(6) DEFAULT NULL,
  `per_day_requirement` int DEFAULT NULL,
  `source` varchar(25) DEFAULT NULL,
  `phoneno_source` bigint DEFAULT NULL,
  PRIMARY KEY (`itemno`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `food_dir`
--

LOCK TABLES `food_dir` WRITE;
/*!40000 ALTER TABLE `food_dir` DISABLE KEYS */;
INSERT INTO `food_dir` VALUES (000001,'Fruits',150,'kg',15,'FreshFarm Pvt Ltd',9876543211),(000002,'Insects',50,'kg',5,'BugBite Suppliers',9123456780),(000003,'Fish',80,'kg',8,'OceanHarvest Co.',9012345678),(000004,'Meat',100,'kg',25,'Carnivore Foods',9087654321),(000005,'Leaves',120,'kg',12,'GreenLeaf Agro',9098765432),(000006,'Bamboo',200,'kg',20,'EcoBamboo Ltd',9023456789);
/*!40000 ALTER TABLE `food_dir` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notes`
--

DROP TABLE IF EXISTS `notes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notes` (
  `userid` varchar(20) NOT NULL,
  `request` varchar(480) DEFAULT 'NA',
  `note` varchar(480) DEFAULT 'NA',
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notes`
--

LOCK TABLES `notes` WRITE;
/*!40000 ALTER TABLE `notes` DISABLE KEYS */;
INSERT INTO `notes` VALUES ('deepikar','NA','NA'),('imrans','sample request','ask for leave next week.'),('meeraj','NA','NA'),('mikee','NA','plan and make advertisements pamphlets'),('nishat','NA','1. check and update new salaries according to govt policies\n2. backup records from pawcache db\n3. complate add staff\n4. change tables for analytical plots\n5. complete analytical plots'),('priyad','NA','NA'),('raviv','NA','NA'),('sandeepk','NA','NA'),('udaans','glass cleaning of store required.','sort items in front top shelf');
/*!40000 ALTER TABLE `notes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `notes_for_deepikar`
--

DROP TABLE IF EXISTS `notes_for_deepikar`;
/*!50001 DROP VIEW IF EXISTS `notes_for_deepikar`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `notes_for_deepikar` AS SELECT 
 1 AS `note`,
 1 AS `request`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `notes_for_imrans`
--

DROP TABLE IF EXISTS `notes_for_imrans`;
/*!50001 DROP VIEW IF EXISTS `notes_for_imrans`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `notes_for_imrans` AS SELECT 
 1 AS `note`,
 1 AS `request`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `notes_for_mayar`
--

DROP TABLE IF EXISTS `notes_for_mayar`;
/*!50001 DROP VIEW IF EXISTS `notes_for_mayar`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `notes_for_mayar` AS SELECT 
 1 AS `note`,
 1 AS `request`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `notes_for_meeraj`
--

DROP TABLE IF EXISTS `notes_for_meeraj`;
/*!50001 DROP VIEW IF EXISTS `notes_for_meeraj`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `notes_for_meeraj` AS SELECT 
 1 AS `note`,
 1 AS `request`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `notes_for_mikee`
--

DROP TABLE IF EXISTS `notes_for_mikee`;
/*!50001 DROP VIEW IF EXISTS `notes_for_mikee`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `notes_for_mikee` AS SELECT 
 1 AS `note`,
 1 AS `request`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `notes_for_nishat`
--

DROP TABLE IF EXISTS `notes_for_nishat`;
/*!50001 DROP VIEW IF EXISTS `notes_for_nishat`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `notes_for_nishat` AS SELECT 
 1 AS `note`,
 1 AS `request`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `notes_for_raviv`
--

DROP TABLE IF EXISTS `notes_for_raviv`;
/*!50001 DROP VIEW IF EXISTS `notes_for_raviv`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `notes_for_raviv` AS SELECT 
 1 AS `note`,
 1 AS `request`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `notes_for_sandeepk`
--

DROP TABLE IF EXISTS `notes_for_sandeepk`;
/*!50001 DROP VIEW IF EXISTS `notes_for_sandeepk`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `notes_for_sandeepk` AS SELECT 
 1 AS `note`,
 1 AS `request`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `notes_for_udaans`
--

DROP TABLE IF EXISTS `notes_for_udaans`;
/*!50001 DROP VIEW IF EXISTS `notes_for_udaans`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `notes_for_udaans` AS SELECT 
 1 AS `note`,
 1 AS `request`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `requests`
--

DROP TABLE IF EXISTS `requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `requests` (
  `sno` int(4) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `username` varchar(20) DEFAULT NULL,
  `request` varchar(480) DEFAULT NULL,
  `status` varchar(16) DEFAULT 'not read',
  PRIMARY KEY (`sno`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `requests`
--

LOCK TABLES `requests` WRITE;
/*!40000 ALTER TABLE `requests` DISABLE KEYS */;
INSERT INTO `requests` VALUES (0001,'deepikar','We need a more playful environment for all the animals in D block, maybe some swings, or some rocks, and if possible, longer grass in bamboo region of pandas.','read'),(0002,'imrans','Please club the salary of next two months and provide it with salary of this month. This is due to some urgent medical requirement.','accepted'),(0003,'imrans','sample request','not read'),(0004,'udaans','glass cleaning of store required.','not read');
/*!40000 ALTER TABLE `requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `ticketno` int(8) unsigned zerofill NOT NULL,
  `date_and_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `review` varchar(360) DEFAULT NULL,
  `rating` int DEFAULT NULL,
  PRIMARY KEY (`ticketno`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` VALUES (00000001,'2025-05-27 12:58:06','Had an amazing time at the zoo today! The elephants were so majestic.',5),(00000002,'2025-05-27 12:58:06','The new bird exhibit is fantastic. So many colorful species!',5),(00000003,'2025-05-27 12:58:06','My kids loved the petting zoo. A great interactive experience.',5),(00000004,'2025-05-20 06:15:00','The tiger enclosure was a bit crowded, but the tiger looked healthy.',4),(00000005,'2025-05-27 12:58:06','Highly recommend the daily animal feeding shows. Very informative!',5),(00000006,'2025-05-27 12:58:06','The zoo is well-maintained, but some areas felt a bit dated.',4),(00000007,'2025-05-25 10:00:00','So happy to see the conservation efforts highlighted throughout the zoo.',5),(00000008,'2025-05-27 12:58:12','The gift shop had some unique items. A perfect end to our visit.',5),(00000013,'2025-06-24 07:45:30','nice but a little too silent and empty and lacks some crowd and cheerful chaos.',3),(00000018,'2025-06-24 08:30:45','staff is friendly, animals are healthy, zoo is informative, snacks available inside !',5);
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shop_purchase_logs`
--

DROP TABLE IF EXISTS `shop_purchase_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shop_purchase_logs` (
  `ticketno` int(8) unsigned zerofill NOT NULL,
  `shop_no` int DEFAULT NULL,
  `date_and_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `items` varchar(72) DEFAULT NULL,
  `amount` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shop_purchase_logs`
--

LOCK TABLES `shop_purchase_logs` WRITE;
/*!40000 ALTER TABLE `shop_purchase_logs` DISABLE KEYS */;
INSERT INTO `shop_purchase_logs` VALUES (00000003,101,'2025-05-21 04:00:00','((Juice,3),(Cereal,1))',170),(00000004,103,'2025-05-22 08:15:00','((Chips,2),(Soda,4))',220),(00000005,101,'2025-05-23 09:30:00','((Coffee,2),(Sugar,1))',110),(00000007,102,'2025-05-25 06:30:00','((Pasta,3),(Sauce,1))',85),(00000011,103,'2025-06-17 05:52:52','((\'Chips\',14),(\'Soda\',12))',1140),(00000012,103,'2025-06-17 09:58:52','((\'Chips\',2))',120),(00000013,101,'2025-06-17 10:03:49','((\'Cereal\',2))',100),(00000014,102,'2025-06-17 09:46:25','((\'Pasta\',6),(\'Sauce\',1))',145),(00000018,104,'2025-06-17 10:05:43','((\'Juice\',1))',40),(00000018,101,'2025-06-22 12:39:06','((\'Pepsi(2L)\',1))',100);
/*!40000 ALTER TABLE `shop_purchase_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shop_stock`
--

DROP TABLE IF EXISTS `shop_stock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shop_stock` (
  `itemno` int(4) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `itemname` varchar(25) DEFAULT NULL,
  `price` int DEFAULT NULL,
  `in_stock` int DEFAULT NULL,
  `required` char(1) DEFAULT 'n',
  `shop_no` int(2) unsigned zerofill DEFAULT NULL,
  PRIMARY KEY (`itemno`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shop_stock`
--

LOCK TABLES `shop_stock` WRITE;
/*!40000 ALTER TABLE `shop_stock` DISABLE KEYS */;
INSERT INTO `shop_stock` VALUES (0001,'Juice',40,20,'n',101),(0002,'Juice',40,0,'y',102),(0003,'Juice',40,8,'y',104),(0004,'Cereal',50,12,'y',101),(0005,'Chips',60,30,'n',103),(0006,'Soda',25,6,'y',103),(0007,'Coffee',35,0,'y',101),(0008,'Sugar',40,15,'n',101),(0009,'Pasta',20,3,'y',102),(0010,'Pasta',20,18,'n',104),(0011,'Sauce',25,10,'n',102),(0012,'Pepsi(2L)',100,20,'n',101);
/*!40000 ALTER TABLE `shop_stock` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff_attendance`
--

DROP TABLE IF EXISTS `staff_attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staff_attendance` (
  `date` date NOT NULL,
  `anjalim` char(1) DEFAULT NULL,
  `raviv` char(1) DEFAULT NULL,
  `priyad` char(1) DEFAULT NULL,
  `amitabhk` char(1) DEFAULT NULL,
  `sonalb` char(1) DEFAULT NULL,
  `imrans` char(1) DEFAULT NULL,
  `deepikar` char(1) DEFAULT NULL,
  `karani` char(1) DEFAULT NULL,
  `meeraj` char(1) DEFAULT NULL,
  `sandeepk` char(1) DEFAULT NULL,
  `nishat` char(1) DEFAULT NULL,
  `rajeshp` char(1) DEFAULT NULL,
  `naveenr` char(1) DEFAULT NULL,
  `ashishn` char(1) DEFAULT NULL,
  `yusufk` char(1) DEFAULT NULL,
  `brahms` char(1) DEFAULT NULL,
  PRIMARY KEY (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff_attendance`
--

LOCK TABLES `staff_attendance` WRITE;
/*!40000 ALTER TABLE `staff_attendance` DISABLE KEYS */;
INSERT INTO `staff_attendance` VALUES ('2025-04-28','P','P','P','P','P','P','P','P','P','P','P','P','P','P','P','P'),('2025-04-29','P','P','P','P','A','P','P','P','P','P','P','P','P','P','P','P'),('2025-04-30','H','H','H','H','H','H','H','H','H','H','H','H','H','H','H','H'),('2025-05-01','P','P','P','P','P','P','P','I','P','P','P','P','P','P','P','P'),('2025-05-02','P','P','P','P','P','P','P','P','P','P','A','P','P','P','P','P'),('2025-05-03','P','P','P','P','P','P','P','P','P','I','P','P','P','P','P','P'),('2025-05-04','P','P','P','P','P','P','P','P','P','P','P','P','P','P','P','P'),('2025-05-05','P','P','I','P','P','P','P','P','P','P','P','P','P','P','P','P'),('2025-05-06','P','P','P','P','P','P','P','P','P','P','P','P','P','P','P','P'),('2025-05-07','H','H','H','H','H','H','H','H','H','H','H','H','H','H','H','H'),('2025-05-08','P','P','P','P','P','P','P','P','P','P','P','P','P','I','P','P'),('2025-05-09','P','P','P','P','P','P','P','P','P','P','A','P','P','P','P','P'),('2025-05-10','P','P','P','P','P','P','P','P','P','P','P','P','P','P','P','P'),('2025-05-11','P','P','P','P','P','P','P','P','P','P','P','P','P','P','P','P'),('2025-05-12','P','P','P','P','P','P','P','P','P','P','P','P','I','P','P','P'),('2025-05-13','P','P','P','P','P','P','P','P','P','P','P','P','P','P','P','P'),('2025-05-14','H','H','H','H','H','H','H','H','H','H','H','H','H','H','H','H'),('2025-05-15','P','P','P','P','P','P','P','P','P','P','P','P','P','P','P','P'),('2025-05-16','P','P','P','P','P','P','P','P','P','P','P','P','P','P','P','P'),('2025-05-17','P','P','P','P','P','P','A','P','P','P','P','P','P','P','P','P'),('2025-05-18','P','P','P','P','P','P','P','P','P','P','P','P','P','P','P','P'),('2025-05-19','P','P','P','P','P','P','P','P','P','P','P','P','P','P','P','P'),('2025-05-20','P','P','P','P','P','P','P','P','P','P','P','P','P','P','P','P'),('2025-05-21','H','H','H','H','H','H','H','H','H','H','H','H','H','H','H','H');
/*!40000 ALTER TABLE `staff_attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff_dat`
--

DROP TABLE IF EXISTS `staff_dat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staff_dat` (
  `staffid` varchar(20) NOT NULL,
  `name` varchar(30) DEFAULT NULL,
  `job` varchar(20) DEFAULT NULL,
  `block` char(3) DEFAULT 'NA',
  `workdays` varchar(50) DEFAULT '(mon,tue,wed,thur,fri,sat,sun)',
  `workshift` varchar(50) DEFAULT '(10.00,13.00),(14.00,18.00)',
  `salary` int DEFAULT NULL,
  `joindate` date DEFAULT NULL,
  PRIMARY KEY (`staffid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff_dat`
--

LOCK TABLES `staff_dat` WRITE;
/*!40000 ALTER TABLE `staff_dat` DISABLE KEYS */;
INSERT INTO `staff_dat` VALUES ('ashishn','Ashish Kumar Nair','Guard','C03','thu,fri,sat','(10.00,12.00),(14.00,20.00)',29000,'2021-09-18'),('brahms','Brahm Singh Soni','Guard','B03','fri,sat,sun','(20.00,6.00)',31000,'2024-01-10'),('deepikar','Deepika Rathi','Veterinarian','D01','mon,wed,thu','(08.00,12.00),(13.00,17.00)',62000,'2023-07-12'),('imrans','Imran Sheikh','Keeper','C04','sat,sun','(09.00,13.00),(14.00,18.00)',36000,'2024-05-10'),('mayar','Maya Ravi','Admin','NA','Mon,Tue,Wed,Thu,Fri,Sat,Sun','(8.30,16.00)',100000,'2025-06-20'),('meeraj','Meera Joshi','Manager','NA','mon,tue,wed','(08.00,12.00),(13.00,20.00)',75000,'2023-02-10'),('mikee','Mike Elipson','Admin','NA','mon,tue,thur,fri,sat','(10.00,20.00)',100000,'2020-09-01'),('naveenr','Naveen Rawat','Guard','A01','mon,tue,wed','(06.00,12.00),(14.00,16.00)',28000,'2022-06-01'),('nishat','Nisha Tiwari','Manager','NA','sun,mon,tue','(20.00,6.00)',77000,'2024-03-15'),('priyad','Priya Desai','Veterinarian','B02','mon,tue,thu,fri','(09.00,13.00),(14.00,17.00)',61000,'2020-09-01'),('raviv','Ravi Verma','Keeper','A03','tue,thu,sat','(08.00,12.00),(14.00,18.00)',37500,'2022-01-15'),('sandeepk','Sandeep Kumar','Manager','NA','thu,fri,sat','(06.00,13.00),(14.00,18.00)',73000,'2022-12-01'),('sonalb','Sonal Bhatt','Maintenance','C02','mon,tue,wed,thu,fri','(07.00,11.00),(13.00,17.00)',34000,'2019-12-05'),('udaans','Udaan Sharma','Shopkeeper','101','mon,tue,wed,thur,fri,sat,sun','(10.00,18.00)',100000,'2020-09-01'),('yusufk','Yusuf Khan','Guard','D02','tue,wed,thu','(08.00,12.00),(14.00,18.00)',30000,'2023-05-22');
/*!40000 ALTER TABLE `staff_dat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transactions` (
  `transact_no` int(5) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `transaction` varchar(20) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `amount` int DEFAULT NULL,
  PRIMARY KEY (`transact_no`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` VALUES (00001,'Build cage','2024-04-04',-12000),(00002,'Set up board','2024-04-05',-4000),(00003,'Buy grains','2024-04-06',-3500),(00004,'Buy meat','2024-04-07',-5000),(00005,'Buy fish','2024-04-08',-3700),(00006,'Raw material refill','2024-04-09',-4600),(00007,'Buy animals','2024-04-10',-25000),(00008,'Visitor ticket gains','2024-04-11',5200),(00009,'Shop gains','2024-04-11',800),(00010,'Visitor ticket gains','2024-04-13',7200),(00011,'Raw material refill','2024-04-13',-3400),(00012,'Shop gains','2024-04-13',1200),(00013,'Visitor ticket gains','2024-04-15',5800),(00014,'Raw material refill','2024-04-15',-4100),(00015,'Shop gains','2024-04-15',950),(00016,'Visitor ticket gains','2024-04-17',9200),(00017,'Shop gains','2024-04-17',1500),(00018,'Visitor ticket gains','2024-04-19',9700),(00019,'Shop gains','2024-04-19',1100),(00020,'Visitor ticket gains','2024-04-21',10100),(00021,'Shop gains','2024-04-21',1400),(00022,'Visitor ticket gains','2024-04-23',9800),(00023,'Shop gains','2024-04-23',1600),(00024,'Visitor ticket gains','2024-04-25',10300),(00025,'Vet fee','2024-04-25',-1000),(00026,'Shop gains','2024-04-25',1300),(00027,'Visitor ticket gains','2024-04-27',9200),(00028,'Shop gains','2024-04-27',900),(00029,'Visitor ticket gains','2024-04-29',9900),(00030,'Shop gains','2024-04-29',1800),(00031,'Visitor ticket gains','2024-05-01',9700),(00032,'Staff Salary','2024-05-01',-200000),(00033,'Shop gains','2024-05-01',1700),(00034,'Visitor ticket gains','2024-05-03',9100),(00035,'Raw material refill','2024-05-03',-11050),(00036,'Shop gains','2024-05-03',850),(00037,'Visitor ticket gains','2024-05-05',9600),(00038,'Shop gains','2024-05-05',1200),(00039,'Visitor ticket gains','2024-05-07',8700),(00040,'Shop gains','2024-05-07',1050),(00041,'Visitor ticket gains','2024-05-09',9500),(00042,'Shop gains','2024-05-09',1600),(00043,'Visitor ticket gains','2024-05-11',9400),(00044,'Shop gains','2024-05-11',1150),(00045,'Visitor ticket gains','2024-05-13',9200),(00046,'Shop gains','2024-05-13',1750),(00047,'Visitor ticket gains','2024-05-15',9700),(00048,'Shop gains','2024-05-15',1000);
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `visitors`
--

DROP TABLE IF EXISTS `visitors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `visitors` (
  `ticketno` int(8) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `singleticketprice` int DEFAULT '35',
  `visitorsingroup` int DEFAULT NULL,
  `extra_fee` int DEFAULT '0',
  `ticketamount` int DEFAULT '0',
  `donation` int DEFAULT '0',
  `phoneno` bigint DEFAULT NULL,
  `date_and_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `paymentmode` varchar(6) DEFAULT 'cash',
  `got_to_know_by` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`ticketno`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `visitors`
--

LOCK TABLES `visitors` WRITE;
/*!40000 ALTER TABLE `visitors` DISABLE KEYS */;
INSERT INTO `visitors` VALUES (00000009,30,1,0,30,0,9876543210,'2025-04-24 06:00:00','cash',NULL),(00000010,30,2,0,60,0,9876543211,'2025-04-24 09:50:00','web','Friends'),(00000011,30,3,0,90,0,9876543212,'2025-04-25 04:30:00','UPI',NULL),(00000012,30,5,0,150,0,9876543213,'2025-04-25 09:15:00','cash','Social Media'),(00000013,30,8,0,240,20,NULL,'2025-04-26 07:00:00','web','Website'),(00000014,30,1,0,30,0,9876543215,'2025-04-26 08:10:00','UPI',NULL),(00000015,30,6,0,180,0,9876543216,'2025-04-27 03:30:00','cash',NULL),(00000016,30,4,0,120,50,NULL,'2025-04-27 05:00:00','web',NULL),(00000017,30,7,0,210,0,9876543218,'2025-04-28 05:45:00','cash',NULL),(00000018,30,2,0,60,0,9876543219,'2025-04-28 09:55:00','UPI',NULL),(00000019,30,20,0,600,100,NULL,'2025-04-29 04:00:00','web','Repeat Visitor'),(00000020,30,22,0,660,0,9876543221,'2025-04-29 04:00:00','card',NULL),(00000021,35,1,0,35,0,9123456789,'2025-05-01 05:30:00','cash','Word of Mouth'),(00000022,35,2,80,150,0,9123456790,'2025-05-01 05:30:00','web',NULL),(00000023,35,3,0,105,0,9123456791,'2025-05-02 07:50:00','UPI','Advertisement'),(00000024,35,5,0,175,0,9123456792,'2025-05-02 08:30:00','cash',NULL),(00000025,35,8,0,280,200,NULL,'2025-05-03 05:00:00','web',NULL),(00000026,35,6,80,290,0,9123456794,'2025-05-03 06:15:00','UPI','Social Media'),(00000027,35,1,0,35,0,9123456795,'2025-05-04 03:30:00','cash','Staff Recommendation'),(00000028,35,4,0,140,0,NULL,'2025-05-04 04:45:00','web',NULL),(00000029,35,7,0,245,0,9123456797,'2025-05-05 07:15:00','UPI','Online Ad'),(00000030,35,22,80,850,0,9123456798,'2025-05-05 07:30:00','card',NULL),(00000031,35,2,0,70,0,9123456799,'2025-05-06 09:00:00','web','Social Media'),(00000032,35,5,0,175,0,9123456700,'2025-05-06 09:15:00','cash',NULL),(00000033,35,3,0,105,80,9123456701,'2025-05-07 04:30:00','UPI',NULL),(00000034,35,3,100,205,0,NULL,'2025-06-12 15:03:21','Web','Youtube'),(00000035,35,2,100,170,0,9823747673,'2025-06-12 15:04:17','Cash','Youtube'),(00000037,35,3,0,105,50,7324876820,'2025-06-12 15:05:31','Cash','Website'),(00000038,35,2,100,170,20,NULL,'2025-06-12 15:13:34','Cash','Repeat Visitor'),(00000039,35,36,2200,3460,10,8888444332,'2025-06-12 15:15:02','UPI','Association contact'),(00000040,35,2,100,170,0,NULL,'2025-06-12 15:26:55','UPI',NULL);
/*!40000 ALTER TABLE `visitors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `notes_for_deepikar`
--

/*!50001 DROP VIEW IF EXISTS `notes_for_deepikar`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `notes_for_deepikar` AS select `notes`.`note` AS `note`,`notes`.`request` AS `request` from `notes` where (`notes`.`userid` = 'deepikar') */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `notes_for_imrans`
--

/*!50001 DROP VIEW IF EXISTS `notes_for_imrans`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `notes_for_imrans` AS select `notes`.`note` AS `note`,`notes`.`request` AS `request` from `notes` where (`notes`.`userid` = 'imrans') */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `notes_for_mayar`
--

/*!50001 DROP VIEW IF EXISTS `notes_for_mayar`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `notes_for_mayar` AS select `notes`.`note` AS `note`,`notes`.`request` AS `request` from `notes` where (`notes`.`userid` = 'mayar') */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `notes_for_meeraj`
--

/*!50001 DROP VIEW IF EXISTS `notes_for_meeraj`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `notes_for_meeraj` AS select `notes`.`note` AS `note`,`notes`.`request` AS `request` from `notes` where (`notes`.`userid` = 'meeraj') */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `notes_for_mikee`
--

/*!50001 DROP VIEW IF EXISTS `notes_for_mikee`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `notes_for_mikee` AS select `notes`.`note` AS `note`,`notes`.`request` AS `request` from `notes` where (`notes`.`userid` = 'mikee') */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `notes_for_nishat`
--

/*!50001 DROP VIEW IF EXISTS `notes_for_nishat`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `notes_for_nishat` AS select `notes`.`note` AS `note`,`notes`.`request` AS `request` from `notes` where (`notes`.`userid` = 'nishat') */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `notes_for_raviv`
--

/*!50001 DROP VIEW IF EXISTS `notes_for_raviv`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `notes_for_raviv` AS select `notes`.`note` AS `note`,`notes`.`request` AS `request` from `notes` where (`notes`.`userid` = 'raviv') */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `notes_for_sandeepk`
--

/*!50001 DROP VIEW IF EXISTS `notes_for_sandeepk`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `notes_for_sandeepk` AS select `notes`.`note` AS `note`,`notes`.`request` AS `request` from `notes` where (`notes`.`userid` = 'sandeepk') */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `notes_for_udaans`
--

/*!50001 DROP VIEW IF EXISTS `notes_for_udaans`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `notes_for_udaans` AS select `notes`.`note` AS `note`,`notes`.`request` AS `request` from `notes` where (`notes`.`userid` = 'udaans') */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-24 14:43:56
