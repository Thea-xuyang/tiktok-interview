-- 1. 先创建图书管理专用数据库，切换进去
CREATE DATABASE IF NOT EXISTS library_management;
USE library_management;

-- 2. 用户表 `user`
CREATE TABLE `user` (
  `user_id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
  `username` VARCHAR(20) NOT NULL UNIQUE COMMENT '用户名/学号',
  `password` VARCHAR(50) NOT NULL COMMENT '登录密码',
  `role` ENUM('学生','管理员') DEFAULT '学生' COMMENT '角色',
  `phone` VARCHAR(11) COMMENT '手机号',
  `register_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
  `status` TINYINT DEFAULT 1 COMMENT '状态：1正常 0禁用'
);

-- 3. 图书分类表 `category`
CREATE TABLE `category` (
  `category_id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '分类ID',
  `category_name` VARCHAR(30) NOT NULL UNIQUE COMMENT '分类名称',
  `description` VARCHAR(100) COMMENT '分类说明',
  `status` TINYINT DEFAULT 1 COMMENT '状态：1启用 0禁用'
);

-- 4. 图书信息表 `book`（核心业务表）
CREATE TABLE `book` (
  `book_id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '图书ID',
  `book_name` VARCHAR(100) NOT NULL COMMENT '书名',
  `author` VARCHAR(50) NOT NULL COMMENT '作者',
  `publisher` VARCHAR(50) COMMENT '出版社',
  `publish_date` DATE COMMENT '出版日期',
  `category_id` INT COMMENT '所属分类ID',
  `isbn` VARCHAR(20) UNIQUE COMMENT 'ISBN编号',
  `price` DECIMAL(10,2) COMMENT '定价',
  `stock` INT DEFAULT 1 COMMENT '库存数量',
  `status` ENUM('在馆','借出','遗失') DEFAULT '在馆' COMMENT '图书状态',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '录入时间',
  FOREIGN KEY (`category_id`) REFERENCES `category`(`category_id`)
);

-- 5. 借阅记录表 `borrow_record`
CREATE TABLE `borrow_record` (
  `record_id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '记录ID',
  `user_id` INT NOT NULL COMMENT '借阅用户ID',
  `book_id` INT NOT NULL COMMENT '借阅图书ID',
  `borrow_time` DATETIME NOT NULL COMMENT '借阅时间',
  `due_time` DATETIME NOT NULL COMMENT '应还时间',
  `return_time` DATETIME COMMENT '实际归还时间',
  `status` ENUM('未还','已还','逾期') DEFAULT '未还' COMMENT '借阅状态',
  `remark` VARCHAR(100) COMMENT '备注',
  FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`),
  FOREIGN KEY (`book_id`) REFERENCES `book`(`book_id`)
);

-- 6. 操作日志表 `operation_log`
CREATE TABLE `operation_log` (
  `log_id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '日志ID',
  `user_id` INT COMMENT '操作用户ID',
  `action` VARCHAR(50) NOT NULL COMMENT '操作类型：新增/修改/删除/查询',
  `detail` TEXT COMMENT '操作详情',
  `ip_address` VARCHAR(50) COMMENT '操作IP',
  `log_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
  FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`)
);