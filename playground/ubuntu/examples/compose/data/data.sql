-- MySQL dump 10.13  Distrib 8.0.19, for Linux (x86_64)
--
-- Host: localhost    Database: example
-- ------------------------------------------------------
-- Server version	8.0.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping data for table `node_tree`
--

LOCK TABLES `node_tree` WRITE;
/*!40000 ALTER TABLE `node_tree` DISABLE KEYS */;
INSERT INTO `node_tree` VALUES (1,2,2,3),(2,2,4,5),(3,2,6,7),(4,2,8,9),(5,1,1,24),(6,2,10,11),(7,2,12,19),(8,3,15,16),(9,3,17,18),(10,2,20,21),(11,3,13,14),(12,2,22,23);
/*!40000 ALTER TABLE `node_tree` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `node_tree_names`
--

LOCK TABLES `node_tree_names` WRITE;
/*!40000 ALTER TABLE `node_tree_names` DISABLE KEYS */;
INSERT INTO `node_tree_names` VALUES (1,1,'english','Marketing'),(2,1,'italian','Marketing'),(3,2,'english','Helpdesk'),(4,2,'italian','Supporto tecnico'),(5,3,'english','Managers'),(6,3,'italian','Managers'),(7,4,'english','Customer Account'),(8,4,'italian','Assistenza Cliente'),(9,5,'english','Docebo'),(10,5,'italian','Docebo'),(11,6,'english','Accounting'),(12,6,'italian','Amministrazione'),(13,7,'english','Sales'),(14,7,'italian','Supporto Vendite'),(15,8,'english','Italy'),(16,8,'italian','Italia'),(17,9,'english','Europe'),(18,9,'italian','Europa'),(19,10,'english','Developers'),(20,10,'italian','Sviluppatori'),(21,11,'english','North America'),(22,11,'italian','Nord America'),(23,12,'english','Quality Assurance'),(24,12,'italian','Controllo Qualità');
/*!40000 ALTER TABLE `node_tree_names` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-06-13  7:44:09
