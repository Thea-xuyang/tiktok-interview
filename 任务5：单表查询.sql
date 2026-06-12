SELECT book_id, book_name, price FROM book;
SELECT * FROM user WHERE role = '管理员';
SELECT * FROM book WHERE price BETWEEN 30 AND 100;
SELECT * FROM book WHERE book_name LIKE '%Python%';
SELECT * FROM borrow_record WHERE user_id=2 AND status='未还';
SELECT * FROM book ORDER BY price DESC;
SELECT COUNT(*) AS 图书总数 FROM book;
SELECT category_id, COUNT(*) AS 图书数量 FROM book GROUP BY category_id;