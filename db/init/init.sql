CREATE DATABASE IF NOT EXISTS project;
use project;

DROP TABLE IF EXISTS `farmers`;

CREATE TABLE `farmers` (
  `email` varchar(50) NOT NULL,
  `firstname` varchar(50) DEFAULT NULL,
  `lastname` varchar(50) DEFAULT NULL,
  `farmname` varchar(50) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`email`),
  UNIQUE KEY `PK_tbl_farmer` (`email`)
) ENGINE=InnoDB;

insert into farmers (email, firstname, lastname, farmname, address)
values ('test@example.com', 'Roy','Leem','Leem Farm', '145 Lint Road');