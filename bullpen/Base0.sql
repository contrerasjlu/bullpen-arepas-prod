CREATE DATABASE  IF NOT EXISTS `bullpen` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `bullpen`;
-- MySQL dump 10.13  Distrib 5.5.46, for debian-linux-gnu (x86_64)
--
-- Host: 127.0.0.1    Database: bullpen
-- ------------------------------------------------------
-- Server version	5.5.46-0ubuntu0.14.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ordertogo_locationsavailable`
--

DROP TABLE IF EXISTS `ordertogo_locationsavailable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ordertogo_locationsavailable` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(100) NOT NULL,
  `location` varchar(1000) NOT NULL,
  `zip_code` varchar(4) NOT NULL,
  `x_coord` varchar(50) NOT NULL,
  `y_coord` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordertogo_locationsavailable`
--

LOCK TABLES `ordertogo_locationsavailable` WRITE;
/*!40000 ALTER TABLE `ordertogo_locationsavailable` DISABLE KEYS */;
INSERT INTO `ordertogo_locationsavailable` VALUES (1,'Truck','Mobile','0000','0000','0000'),(2,'Mall Duluth','5900 Sugarloaf Pkwy, Lawrenceville, GA 30043','3307','12345','123654'),(3,'Mall of Georgia','1280 Jardin Ct','3307','','');
/*!40000 ALTER TABLE `ordertogo_locationsavailable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `LocationManager_location_admin_menu`
--

DROP TABLE IF EXISTS `LocationManager_location_admin_menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `LocationManager_location_admin_menu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `label` varchar(50) NOT NULL,
  `url` varchar(50) DEFAULT NULL,
  `imgClass` varchar(50) DEFAULT NULL,
  `activeOn` varchar(20) DEFAULT NULL,
  `order` int(11) NOT NULL,
  `child_of` varchar(20),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LocationManager_location_admin_menu`
--

LOCK TABLES `LocationManager_location_admin_menu` WRITE;
/*!40000 ALTER TABLE `LocationManager_location_admin_menu` DISABLE KEYS */;
INSERT INTO `LocationManager_location_admin_menu` VALUES (1,'Locations Available','LocationManager:locations-list','fa fa-truck','locations_',1,'None'),(2,'Payment Batches','LocationManager:batches-list','fa fa-edit','batches',2,'None'),(3,'Orders','LocationManager:orders','fa fa-desktop','orders',3,'None');
/*!40000 ALTER TABLE `LocationManager_location_admin_menu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ordertogo_genericvariable`
--

DROP TABLE IF EXISTS `ordertogo_genericvariable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ordertogo_genericvariable` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(45) NOT NULL,
  `value` varchar(500) NOT NULL,
  `description` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ordertogo_genericvariable_code_67eafc9ecdea0838_uniq` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordertogo_genericvariable`
--

LOCK TABLES `ordertogo_genericvariable` WRITE;
/*!40000 ALTER TABLE `ordertogo_genericvariable` DISABLE KEYS */;
INSERT INTO `ordertogo_genericvariable` VALUES (1,'tax.percent','0.07','Tax percent for the whole site'),(2,'delivery.cost','0','Cost per order for delivery'),(3,'google.API.KEY','AIzaSyDP6kgI98A7QW3vc2HR3l-BWHnr0lUbMH4','API Key para la consulta en los servicios de '),(4,'pay.apikey','y6pWAJNyJyjGv66IsVuWnklkKUPFbb0a','Api Key para Payeezy'),(5,'pay.secret','86fbae7030253af3cd15faef2a1f4b67353e41fb6799f576b5093ae52901e6f7','Secret Key de Payeezy'),(6,'pay.token','fdoa-a480ce8951daa73262734cf102641994c1e55e7cdf4c02b6','Token de Payeezy'),(7,'pay.url','https://api-cert.payeezy.com/v1/transactions','URL de Prueba de Payeezy');
/*!40000 ALTER TABLE `ordertogo_genericvariable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ordertogo_paymentbatch`
--

DROP TABLE IF EXISTS `ordertogo_paymentbatch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ordertogo_paymentbatch` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime NOT NULL,
  `max_miles` int(11) NOT NULL,
  `batch_code` varchar(10) NOT NULL,
  `status` varchar(1) NOT NULL,
  `time_to_close` time NOT NULL,
  `open_for_delivery` tinyint(1) NOT NULL,
  `address_for_truck` varchar(1000) NOT NULL,
  `location_id` int(11) NOT NULL,
  `zip_code_for_truck` varchar(4) NOT NULL,
  `close_date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `batch_code` (`batch_code`),
  KEY `ordertogo_paymentbatch_e274a5da` (`location_id`),
  CONSTRAINT `location_id_5991f4938ea1b97f_fk_ordertogo_locationsavailable_id` FOREIGN KEY (`location_id`) REFERENCES `ordertogo_locationsavailable` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordertogo_paymentbatch`
--

LOCK TABLES `ordertogo_paymentbatch` WRITE;
/*!40000 ALTER TABLE `ordertogo_paymentbatch` DISABLE KEYS */;
INSERT INTO `ordertogo_paymentbatch` VALUES (1,'2015-11-04 00:00:00',10,'2015-23','O','00:22:00',1,'5900 Sugarloaf Pkwy, Lawrenceville, GA 30043',2,'3302','2015-12-01 02:11:06'),(2,'2015-11-04 00:00:00',20,'2015-27','O','22:00:00',1,'2500 Buford Dr NE, Lawrenceville, GA 30043',1,'3302','2015-11-30 00:07:25'),(3,'2015-11-25 00:00:00',89,'2015-98','C','23:34:45',1,'',2,'','2015-11-28 02:36:18'),(4,'2015-11-26 00:00:00',23,'2015-78','C','00:06:48',1,'2300 hialiadh',1,'2345','2015-11-28 02:36:18'),(5,'2015-11-28 02:37:57',20,'2015-29','C','22:07:57',1,'',3,'','2015-11-28 02:38:49'),(6,'2015-11-28 14:47:40',23,'2015-80','C','10:17:40',1,'Acuarelas Del Sol Parque Esmeralda',1,'4001','2015-11-28 18:10:24');
/*!40000 ALTER TABLE `ordertogo_paymentbatch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ordertogo_product`
--

DROP TABLE IF EXISTS `ordertogo_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ordertogo_product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(50) NOT NULL,
  `name` varchar(80) NOT NULL,
  `description` longtext NOT NULL,
  `price` decimal(19,2) NOT NULL,
  `Active` tinyint(1) NOT NULL,
  `category_id` int(11) NOT NULL,
  `extras` int(11) NOT NULL,
  `order_in_menu` int(11) NOT NULL,
  `image` varchar(100) NOT NULL,
  `allow_paid_extras` tinyint(1) NOT NULL,
  `allow_sauces` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `ordertogo__category_id_48b5c168bf01e9c6_fk_ordertogo_category_id` (`category_id`),
  CONSTRAINT `ordertogo__category_id_48b5c168bf01e9c6_fk_ordertogo_category_id` FOREIGN KEY (`category_id`) REFERENCES `ordertogo_category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordertogo_product`
--

LOCK TABLES `ordertogo_product` WRITE;
/*!40000 ALTER TABLE `ordertogo_product` DISABLE KEYS */;
INSERT INTO `ordertogo_product` VALUES (1,'pl.1','Hit','With 1 PLAYER OF YOUR CHOICE',4.90,1,3,1,1,'',1,1),(2,'pl.2','Double','With 2 PLAYER OF YOUR CHOICE',5.90,1,3,2,2,'',1,1),(3,'pl.3','Triple','With 3 PLAYERS OF YOUR CHOICE',6.90,1,3,3,3,'',1,1),(4,'pl.4','Home Run','With 4 PLAYERS OF YOUR CHOICE',7.50,1,3,4,4,'',1,1),(5,'pl.5','Home Run Pabellon','With 4 VENEZUELAN PLAYERS',8.70,1,3,0,5,'',1,1),(6,'pl.6','Grand Slam','With 5 VENEZUELAN PLAYERS OF YOUR CHOICE',8.50,1,3,5,6,'',1,1),(7,'1B','Shredded meat','Carne Mechada',0.00,1,4,0,1,'',1,1),(8,'2B','Shredded chicken','Pollo Mechado',0.00,1,4,0,2,'',1,1),(9,'SS','Pulled Pork','Pernil',0.00,1,4,0,3,'',1,1),(10,'3B','Fish','Pescado',0.00,1,4,0,4,'',1,1),(11,'LF','Chicken Salad','Reina Pepiada',0.00,1,4,0,5,'',0,0),(12,'CF','Ham','Jamón',0.00,1,4,0,6,'',0,0),(13,'RF','Black Beans','Caraotas Negras',0.00,1,4,0,7,'',0,0),(14,'DH','American Cheese','Queso Americano',0.00,1,4,0,8,'',0,0),(15,'C','Fresh Cheese','Queso Fresco',0.00,1,4,0,9,'',0,0),(16,'ob.1','Acocado','Aguacate',0.99,1,8,0,1,'',1,1),(17,'ob.2','Eggs','Huevos',0.99,1,8,0,2,'',1,1),(18,'ob.3','Sweet fried plantains','Platano Maduro Frito',0.99,1,8,0,3,'',1,1),(19,'ll.1','Mini Bats','With 5 Cheese Sticks',3.99,1,5,0,1,'',0,0),(20,'ll.2','Mini Ball','With 6 Corn Cheese balls',3.99,1,5,0,2,'',0,0),(21,'ll.3','Swing Spread','Ham Spread Arepa',3.99,1,5,0,3,'',0,0),(22,'sd.1','Soda','Soda',1.00,1,6,0,1,'',1,1),(23,'sd.2','Water','Water',1.00,1,6,0,2,'',1,1),(24,'sd.3','Juice','Juice',1.00,1,6,0,3,'',1,1),(25,'sa.1','Strike','Guasacaca',0.00,1,7,0,1,'',1,1),(26,'sa.2','Rolling','Tartar',0.00,1,7,0,2,'',1,1),(27,'sa.3','Swing','Pink',0.00,1,7,0,3,'',1,1),(28,'sa.4','Wild Pitch','Hot & Spicy',0.00,1,7,0,4,'',1,1),(30,'ob.1B','Shredded meat','Carne Mechada',0.99,1,8,0,4,'',1,1),(31,'ob.2B','Shredded chicken','Pollo Mechado',0.99,1,8,1,5,'',1,1),(32,'ob.SS','Pulled Pork','Pernil',0.99,1,8,1,6,'',1,1),(33,'ob.3B','Fish','Pescado',0.99,1,8,1,7,'',1,1),(34,'ob.LF','Chicken Salad','Reina Pepiada',0.99,1,8,1,8,'',1,1),(35,'ob.CF','Ham','Jamón',0.99,1,8,1,9,'',1,1),(36,'ob.RF','Black Beans','Caraotas Negras',0.99,1,8,1,10,'',1,1),(37,'ob.DH','American Cheese','Queso Americano',0.99,1,8,1,11,'',1,1),(38,'ob.C','Fresh Cheese','Queso Fresco',0.99,1,8,0,12,'',0,0);
/*!40000 ALTER TABLE `ordertogo_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ordertogo_category`
--

DROP TABLE IF EXISTS `ordertogo_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ordertogo_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` longtext NOT NULL,
  `Active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordertogo_category`
--

LOCK TABLES `ordertogo_category` WRITE;
/*!40000 ALTER TABLE `ordertogo_category` DISABLE KEYS */;
INSERT INTO `ordertogo_category` VALUES (3,'arepas','Baked or Fried Arepas','Default Category',1),(4,'extras','Line Up Players','Extras',1),(5,'kids','Little League','Kid\'s Meal',1),(6,'drinks','Soft Drinks','Drinks',1),(7,'sauces','Sauces','Sauces',1),(8,'paid.extras','On the Bench','Paid Extras',1);
/*!40000 ALTER TABLE `ordertogo_category` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-11-30 22:28:01
