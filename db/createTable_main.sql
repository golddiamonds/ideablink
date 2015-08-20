delimiter $$

CREATE TABLE `main` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `entry_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `entry_link` tinyblob,
  `entry_blurb` tinytext,
  `userid` int(11) DEFAULT NULL,
  `username` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8$$

