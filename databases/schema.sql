


CREATE TABLE `courses` (
  `courses_id` int NOT NULL AUTO_INCREMENT,
  `course_name` varchar(90) NOT NULL,
  `course_level` enum('Undergraduate','Postgraduate','HND','PhD') NOT NULL,
  `course_description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
  `duration_years` int NOT NULL,
  PRIMARY KEY (`courses_id`)