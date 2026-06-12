SELECT * FROM user WHERE user_id = 1;

UPDATE user 
SET phone = '13900139000' 
WHERE user_id = 1;

SELECT * FROM user WHERE user_id = 1;


SELECT * FROM book WHERE status = '借出';

SET SQL_SAFE_UPDATES = 0;
UPDATE book 
SET status = '在馆' 
WHERE status = '借出';
SET SQL_SAFE_UPDATES = 1;

SELECT * FROM book WHERE status = '在馆';


SELECT book_name, price FROM book WHERE price > 50;

SET SQL_SAFE_UPDATES = 0;
UPDATE book 
SET price = price * 0.9 
WHERE price > 50;
SET SQL_SAFE_UPDATES = 1;

SELECT book_name, price FROM book WHERE price > 0;


SELECT * FROM borrow_record WHERE status = '未还';

SET SQL_SAFE_UPDATES = 0;
UPDATE borrow_record 
SET status = '已还', return_time = NOW() 
WHERE record_id = 1;
SET SQL_SAFE_UPDATES = 1;

SELECT * FROM borrow_record WHERE record_id = 1;

SET SQL_SAFE_UPDATES = 0;
UPDATE book 
SET category_id = 999 
WHERE book_id = 1; 
SET SQL_SAFE_UPDATES = 1;