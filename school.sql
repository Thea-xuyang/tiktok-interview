-- 创建数据库
CREATE DATABASE IF NOT EXISTS `school_management`;
USE `school_management`;

-- 创建学生表
CREATE TABLE IF NOT EXISTS `student` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  `gender` CHAR(1),
  `birth_date` DATE
);