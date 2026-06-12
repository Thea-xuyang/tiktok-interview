INSERT INTO user(username,password,role) VALUES('temp_user','123456','学生');
SELECT * FROM user WHERE username='temp_user';

DELETE FROM user WHERE username='temp_user';
SELECT * FROM user WHERE username='temp_user';

SELECT COUNT(*) AS 日志总数 FROM operation_log;
SET SQL_SAFE_UPDATES = 0;
DELETE FROM operation_log WHERE log_id < 3;
SET SQL_SAFE_UPDATES = 1;
SELECT COUNT(*) AS 日志总数 FROM operation_log;

DELETE FROM category WHERE category_id = 1;