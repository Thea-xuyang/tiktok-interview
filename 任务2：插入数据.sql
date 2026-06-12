
INSERT INTO user(username,password,role) VALUES('stu_test01','test123','学生');
SELECT * FROM user WHERE username='stu_test01';

INSERT INTO user(username,password) VALUES('stu_test02','test123');
SELECT * FROM user WHERE username='stu_test02';

INSERT INTO category(category_name) VALUES('历史'),('哲学'),('艺术');
SELECT * FROM category WHERE category_name IN ('历史','哲学','艺术');

INSERT INTO user(username,password) VALUES('admin01','123456');