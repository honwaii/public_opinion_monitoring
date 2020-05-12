SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for pom_shop
DROP TABLE IF EXISTS `pom_shop`;
CREATE TABLE `pom_shop` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `shop_name` varchar(255) NOT NULL,
  `user_id` int(11) NOT NULL DEFAULT 6,
  `poi_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=151 DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `pom_shop_comment`;
CREATE TABLE `pom_shop_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `shop_id` int(11) NOT NULL,
  `comment` text DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  `key_word` varchar(255) DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT NULL ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19180 DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `pom_user`;
CREATE TABLE `pom_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4;
