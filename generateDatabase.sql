CREATE DATABASE csdpath;
use csdpath;
-- MariaDB dump 10.19  Distrib 10.5.23-MariaDB, for Linux (x86_64)
--
-- Host: database-1.cvwoaic8ob2d.us-west-1.rds.amazonaws.com    Database: csdpath
-- ------------------------------------------------------
-- Server version	8.0.35

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `classes`
--

DROP TABLE IF EXISTS `classes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `classes` (
  `class_id` int NOT NULL AUTO_INCREMENT,
  `class_code` char(50) NOT NULL,
  `class_name` text,
  `credits` float DEFAULT NULL,
  PRIMARY KEY (`class_id`),
  UNIQUE KEY `class_code` (`class_code`)
) ENGINE=InnoDB AUTO_INCREMENT=131 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classes`
--

LOCK TABLES `classes` WRITE;
/*!40000 ALTER TABLE `classes` DISABLE KEYS */;
INSERT INTO `classes` VALUES (1,'CSD110','CSD 110 Computer Programming Fundamentals with Python',5),(2,'CSD112','CSD 112 HTML and CSS',5),(3,'ENGL&101','ENGL&101 English Composition I',5),(4,'CS&141','CS& 141 Computer Science I Java',5),(5,'CSD122','CSD 122 JavaScript',5),(6,'CSD138','CSD 138 Structured Query Language (SQL)',5),(7,'CS143','CS 143 Computer Science II Java',5),(8,'CSD268','CSD 268 Quality Assurance Methodologies',5),(9,'MATH&141','MATH& 141 Pre-Calculus I',5),(10,'Humanities5_1','Humanities course',5),(11,'NatSci5_1','Natural Science course with a lab',5),(12,'SocSci5_1','Social Science course',5),(13,'CSD230','CSD 230 Programming For Mobile Devices',5),(14,'CSD275','CSD 275 PHP Scripting',5),(15,'CSD233','CSD 233 C++ Programming',5),(16,'CSD228','CSD 228 Programming with C#',5),(17,'CSD298','CSD 298 or DSGN 290 Technical Interview/Job Seach',5),(18,'CSD297','CSD 297 IT Project',3),(19,'TechElec5_1','Technical Elective: choose CSD 235 or CSD 294 or any other CSD',5),(20,'TechElec5_2','Technical Elective: choose CSD 235 or CSD 294 or any other CSD',5),(21,'MATH&151','MATH& 151 Calculus I',5),(22,'Humanities5_2','Humanities course',5),(23,'NatSci5_2','Natural Science course with a lab',5),(24,'CSD322','CSD 322 Computer and Network Architecture',5),(25,'CSD323','CSD323 Data Analytics',5),(26,'MATH220','MATH 220 Linear Algebra',5),(27,'CSD331','CSD 331 Database Modeling and Design',5),(28,'CSD332','CSD 332 Software Project Management',5),(29,'CSD335','CSD 335 Algorithms and Data Structures',5),(30,'CSD412','CSD 412 Web Application Development',5),(31,'CSD415','CSD 415 Operating Systems Concepts',5),(32,'ENGL&235','ENGL& 235 Technical Writing',5),(33,'CSD425','CSD 425 Cloud Computing',5),(34,'CSD436','CSD 436 Algorithmic Problem Solving for Interviews',5),(35,'PHYS&114','PHYS& 114 General Physics I w/Lab',5),(36,'CSD438','CSD 438 Big Data Application Development',5),(37,'CSD480','CSD 480 Capstone Project',5),(38,'PSYC324','PSYC 324 Psychology of Organizations',5),(39,'CS101','CS 101 Introduction to Computer Science',5),(40,'CS102','CS 102 Computer Science Careers/Student Success',5),(41,'ENGL&102','ENGL&102 English Composition II (or ENGL& 235 Technical Writing)',5),(42,'MATH&142','MATH&142 Pre-Calculus II',5),(43,'SocSci5_2','Social Science course',5),(44,'CS170','CS 170 Linear Algebra for Data Analysis',5),(45,'CS222','CS 222 Computing, Data, and Society',5),(46,'CS233','CS233 Web and Database Programming',5),(47,'CS296','CS296 Computer Science Career Seminar',2),(48,'CS243','CS243 Software Development Tools',3),(49,'CS202','CS202 Discrete Structures I',5),(50,'CS301','CS301 Foundations of Computer Science',5),(51,'CS321','CS321 Database Systems',5),(52,'CS397','CS397 Computer Science Seminar I',1),(53,'CS302','CS302 Discrete Structures II',5),(54,'CS333','CS333 Data Structures and Algorithms I',5),(55,'CS334','CS334 Data Structures & Algorithms II',5),(56,'CS350','CS350 Software Engineering',5),(57,'CS398','CS398 Computer Science Seminar II',1),(58,'CS421','CS421 Algorithmic Problem Solving',5),(59,'CS442','CS442 Principles of Computer Systems',5),(60,'CS498','CS498 Computer Science Seminar III',1),(61,'CS485','CS 485 Capstone Project I',5),(62,'CS433','CS 433 Programming Languages',5),(63,'CS402','CS402 Statistical Methods for Testing',5),(64,'CS486','CS486 Capstone Project II',5),(65,'CS450','CS450 Security Foundations',2),(66,'MATH&152','MATH& 152 Calculus II',5),(67,'SOC&101','SOC& 101 Introduction to Sociology',5),(68,'MATH&163or146','MATH& 163 Intro to Statistics or MATH& 146 Calculus III',5),(69,'PHYS&221','PHYS& 221 Engineering Physics I with Lab',5),(70,'ECON&201','ECON& 201 Micro Economics',5),(71,'PSYC&100','PSYC& 100 General Psychology',5),(72,'MATH&264','MATH& 264 Calculus IV (WSU requirement)',5),(73,'PHYS&222','PHYS& 222 Engineering Physics II with Lab',5),(74,'Humanities5_3','Humanities course',5),(75,'PHIL&120','PHIL& 120 Symbolic Logic (WSU requirement)',5),(76,'ENGL&235orENGL&102orCMST&220','ENGL& 235 or ENGL&102 or CMST& 220',5),(77,'Elec5_1','Elective course (CSD 233 C++ Programming recommended)',5),(78,'Elec5_2','Elective course (MATH& 142 Pre-Calculus II may beused) or BIOL& 160',5),(79,'ENGL93','ENGL 93 (or placement into ENGL 99 or higher)',5),(80,'ENGL99','ENGL 99 Intro to Essay Writing',5),(81,'MATH90','MATH 90 (or placement into MATH 99 or higher)',5),(82,'MATH99','MATH 99 (or placement into MATH& 141))',5),(83,'MATH87','MATH 87 (or placement into MATH 90 or higher)',5),(84,'FinishedAssociate','Completion of Associate Degree',NULL),(85,'GPA','Minimum 2.0 GPA',NULL),(86,'GeneralCredits','Completion of at least 25 General Education course credits',NULL),(87,'AdmissionToBAS','Admission to BAS IT:CSD program',NULL),(88,'MATH98','MATH 98 or MATH 99 (or placement into MATH& 107 or higher)',5),(89,'BSCSenrollment','Upper Division BS Enrollment',NULL);
/*!40000 ALTER TABLE `classes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prerequisites`
--

DROP TABLE IF EXISTS `prerequisites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `prerequisites` (
  `class_id` int NOT NULL,
  `prerequisite_by_class_id` int NOT NULL,
  PRIMARY KEY (`class_id`,`prerequisite_by_class_id`),
  KEY `FK_prerequisites__classes` (`prerequisite_by_class_id`),
  CONSTRAINT `FK_classes_classes` FOREIGN KEY (`class_id`) REFERENCES `classes` (`class_id`),
  CONSTRAINT `FK_prerequisites__classes` FOREIGN KEY (`prerequisite_by_class_id`) REFERENCES `classes` (`class_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prerequisites`
--

LOCK TABLES `prerequisites` WRITE;
/*!40000 ALTER TABLE `prerequisites` DISABLE KEYS */;
INSERT INTO `prerequisites` VALUES (4,1),(5,1),(6,1),(14,1),(44,1),(5,2),(14,2),(32,3),(41,3),(43,3),(45,3),(76,3),(7,4),(8,4),(16,4),(46,4),(24,5),(30,5),(24,6),(27,6),(13,7),(15,7),(17,7),(18,7),(28,7),(29,7),(47,7),(48,7),(50,7),(51,7),(54,7),(24,8),(42,9),(22,10),(23,11),(43,12),(20,19),(66,21),(73,21),(74,22),(31,24),(27,26),(30,27),(36,27),(34,29),(33,30),(36,33),(21,42),(26,42),(69,42),(49,44),(53,49),(54,49),(53,50),(59,50),(55,54),(72,68),(73,69),(1,79),(2,79),(39,79),(67,79),(71,79),(3,80),(70,80),(1,81),(9,82),(43,82),(2,83),(39,83),(71,83),(24,84),(25,84),(27,84),(28,84),(29,84),(30,84),(31,84),(33,84),(34,84),(36,84),(37,84),(38,84),(24,85),(25,85),(27,85),(28,85),(29,85),(30,85),(31,85),(33,85),(34,85),(36,85),(37,85),(38,85),(24,86),(25,86),(27,86),(28,86),(29,86),(30,86),(31,86),(33,86),(34,86),(36,86),(37,86),(38,86),(24,87),(25,87),(27,87),(28,87),(29,87),(30,87),(31,87),(33,87),(34,87),(36,87),(37,87),(38,87),(35,88),(70,88),(75,88),(52,89),(56,89),(57,89),(58,89),(59,89),(60,89),(61,89),(62,89),(63,89),(64,89),(65,89);
/*!40000 ALTER TABLE `prerequisites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `programs`
--

DROP TABLE IF EXISTS `programs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `programs` (
  `program_id` int NOT NULL AUTO_INCREMENT,
  `program_name` varchar(255) NOT NULL,
  PRIMARY KEY (`program_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `programs`
--

LOCK TABLES `programs` WRITE;
/*!40000 ALTER TABLE `programs` DISABLE KEYS */;
INSERT INTO `programs` VALUES (1,'ACS DTA/MRP'),(2,'CSD AAS-T'),(3,'BS'),(4,'BAS');
/*!40000 ALTER TABLE `programs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `programs_classes_quarters`
--

DROP TABLE IF EXISTS `programs_classes_quarters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `programs_classes_quarters` (
  `program_id` int NOT NULL,
  `quarter_no` float NOT NULL,
  `course_id` int NOT NULL,
  PRIMARY KEY (`program_id`,`quarter_no`,`course_id`),
  UNIQUE KEY `program_id` (`program_id`,`course_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `programs_classes_quarters_ibfk_1` FOREIGN KEY (`program_id`) REFERENCES `programs` (`program_id`),
  CONSTRAINT `programs_classes_quarters_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `classes` (`class_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `programs_classes_quarters`
--

LOCK TABLES `programs_classes_quarters` WRITE;
/*!40000 ALTER TABLE `programs_classes_quarters` DISABLE KEYS */;
INSERT INTO `programs_classes_quarters` VALUES (1,1,1),(2,1,1),(3,4,1),(2,1,2),(1,1,3),(2,1,3),(3,1,3),(4,6.5,3),(1,2,4),(2,2,4),(3,5,4),(2,2,5),(4,7,5),(2,2,6),(4,7,6),(1,3,7),(2,3,7),(3,6,7),(4,6.5,7),(2,3,8),(4,7,8),(1,0,9),(2,3,9),(3,2,9),(1,2,10),(2,4,10),(3,2,10),(4,6.5,10),(2,4,11),(3,4,11),(2,4,12),(3,1,12),(4,6.5,12),(2,5,13),(2,5,14),(2,5,15),(2,6,16),(2,6,17),(2,6,18),(2,6,19),(3,11,19),(3,12,20),(1,1,21),(4,7,21),(1,4,22),(3,8,22),(4,7,22),(3,5,23),(4,7,23),(4,8,24),(3,9,25),(4,8,25),(4,8,26),(4,9,27),(4,9,28),(4,9,29),(4,10,30),(4,10,31),(4,10,32),(4,11,33),(4,11,34),(4,11,35),(4,12,36),(4,12,37),(4,12,38),(3,1,39),(3,2,40),(3,3,41),(1,0,42),(3,3,42),(4,6.5,42),(3,3,43),(3,4,44),(3,5,45),(3,6,46),(3,6,47),(3,6,48),(3,7,49),(3,7,50),(3,7,51),(3,7,52),(3,8,53),(3,8,54),(3,9,55),(3,9,56),(3,9,57),(3,10,58),(3,10,59),(3,10,60),(3,11,61),(3,11,62),(3,12,63),(3,12,64),(3,10,65),(1,2,66),(1,3,67),(1,3,68),(1,4,69),(1,5,70),(1,4,71),(1,4,72),(1,5,73),(1,5,74),(1,5,75),(1,6,76),(1,6,77),(1,6,78),(1,0,79),(2,0,79),(3,0,79),(1,0,80),(2,0,80),(3,0,80),(1,0,81),(2,0,81),(1,0,82),(2,0,82),(3,0,82),(1,0,83),(2,0,83),(3,0,83),(4,6.5,84),(4,6.5,85),(4,6.5,86),(4,6.5,87),(1,0,88),(4,6.5,88),(3,6.5,89);
/*!40000 ALTER TABLE `programs_classes_quarters` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `roles` (
  `role_id` int NOT NULL AUTO_INCREMENT,
  `role_description` varchar(50) NOT NULL,
  PRIMARY KEY (`role_id`),
  UNIQUE KEY `role_description` (`role_description`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'admin');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `salt` varchar(255) NOT NULL,
  `role_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `FK_role_id_roles` (`role_id`),
  CONSTRAINT `FK_role_id_roles` FOREIGN KEY (`role_id`) REFERENCES `roles` (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','$2b$07$rsXi5zGA6x7esJuIZp/NWOG2HwPEkNglMvUv.8vUkflwWd6w9IvRa','$2b$07$rsXi5zGA6x7esJuIZp/NWO',1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-29 22:13:24
