SELECT * FROM unlocks LIMIT 10; 

SELECT 
    u.user_id,
    CONCAT(u.model_id, '_', u.ability) AS product_id
FROM 
    unlocks u
INNER JOIN 
    (
        SELECT 
            user_id
        FROM 
            unlocks
        GROUP BY 
            user_id
        HAVING 
            COUNT(*) > 1
    ) ub 
ON u.user_id = ub.user_id
LIMIT 500000;



select * from unlocks where user_id = 13042;

SELECT 
    u.user_id,
    CONCAT(u.model_id, '_', u.ability) AS product_id,
    CASE 
        WHEN u.ability = 'listen' THEN b.title 
        ELSE e.title 
    END AS product_name
FROM 
    unlocks u
INNER JOIN 
    (
        SELECT 
            user_id
        FROM 
            unlocks
        GROUP BY 
            user_id
        HAVING 
            COUNT(*) > 1
    ) ub 
ON u.user_id = ub.user_id
LEFT JOIN 
    books b ON u.model_id = b.audio_book_id AND u.ability = 'listen'
LEFT JOIN 
    books e ON u.model_id = e.ebook_id AND u.ability = 'read'
WHERE 
    (u.ability = 'listen' AND b.title IS NOT NULL) OR 
    (u.ability = 'read' AND e.title IS NOT NULL)
LIMIT 500000;


-- Added author
SELECT 
    u.user_id,
    CONCAT(u.model_id, '_', u.ability) AS product_id,
    CASE 
        WHEN u.ability = 'listen' THEN b.title 
        ELSE e.title 
    END AS product_name,
    COALESCE(b.author_id, e.author_id) AS author_id,
    a.name AS author_name
FROM 
    unlocks u
INNER JOIN 
    (
        SELECT 
            user_id
        FROM 
            unlocks
        GROUP BY 
            user_id
        HAVING 
            COUNT(*) > 1
    ) ub 
ON u.user_id = ub.user_id
LEFT JOIN 
    books b ON u.model_id = b.audio_book_id AND u.ability = 'listen'
LEFT JOIN 
    books e ON u.model_id = e.ebook_id AND u.ability = 'read'
LEFT JOIN
    authors a ON a.id = COALESCE(b.author_id, e.author_id)
WHERE 
    (u.ability = 'listen' AND b.title IS NOT NULL) OR 
    (u.ability = 'read' AND e.title IS NOT NULL)
LIMIT 500000;

-- Added topic
SELECT 
    u.user_id,
    CONCAT(u.model_id, '_', u.ability) AS product_id,
    CASE 
        WHEN u.ability = 'listen' THEN b.title 
        ELSE e.title 
    END AS product_name,
    COALESCE(b.author_id, e.author_id) AS author_id,
    a.name AS author_name,
    t.id AS topic_id,
    t.title AS topic_name
FROM 
    unlocks u
INNER JOIN 
    (
        SELECT 
            user_id
        FROM 
            unlocks
        GROUP BY 
            user_id
        HAVING 
            COUNT(*) > 1
    ) ub 
ON u.user_id = ub.user_id
LEFT JOIN 
    books b ON u.model_id = b.audio_book_id AND u.ability = 'listen'
LEFT JOIN 
    books e ON u.model_id = e.ebook_id AND u.ability = 'read'
LEFT JOIN
    authors a ON a.id = COALESCE(b.author_id, e.author_id)
LEFT JOIN 
    topic_items ti ON (ti.model_id = b.audio_book_id AND ti.model_type = 'audio_book') OR 
                     (ti.model_id = e.ebook_id AND ti.model_type = 'ebook')
LEFT JOIN 
    topics t ON ti.topic_id = t.id
WHERE 
    (u.ability = 'listen' AND b.title IS NOT NULL) OR 
    (u.ability = 'read' AND e.title IS NOT NULL)
LIMIT 500000;


-- Removed useless data
-- Added topic exclusion
SELECT 
    u.user_id,
    CONCAT(u.model_id, '_', u.ability) AS product_id,
    CASE 
        WHEN u.ability = 'listen' THEN b.title 
        ELSE e.title 
    END AS product_name,
    COALESCE(b.author_id, e.author_id) AS author_id,
    a.name AS author_name,
    t.id AS topic_id,
    t.title AS topic_name
FROM 
    unlocks u
INNER JOIN 
    (
        SELECT 
            user_id
        FROM 
            unlocks
        GROUP BY 
            user_id
        HAVING 
            COUNT(*) > 1
    ) ub 
ON u.user_id = ub.user_id
LEFT JOIN 
    books b ON u.model_id = b.audio_book_id AND u.ability = 'listen'
LEFT JOIN 
    books e ON u.model_id = e.ebook_id AND u.ability = 'read'
LEFT JOIN
    authors a ON a.id = COALESCE(b.author_id, e.author_id)
LEFT JOIN 
    topic_items ti ON (ti.model_id = b.audio_book_id AND ti.model_type = 'audio_book') OR 
                     (ti.model_id = e.ebook_id AND ti.model_type = 'ebook')
LEFT JOIN 
    topics t ON ti.topic_id = t.id
WHERE 
    (u.ability = 'listen' AND b.title IS NOT NULL) OR 
    (u.ability = 'read' AND e.title IS NOT NULL)
    AND t.id NOT IN (47, 48, 49, 50, 51)
LIMIT 500000;






-- ['1170_read', '1050_read', '630_read', '1404_read', '1361_read']

select * from books where ebook_id = 1170;
select * from books where ebook_id = 1050;
select * from books where ebook_id = 630;
select * from books where ebook_id = 1404;
select * from books where ebook_id = 1361;


SELECT 
    u.user_id,
    u.model_id,
    u.ability,
    b.title AS book_name
FROM 
    unlocks u
LEFT JOIN 
    books b ON 
        (u.ability = 'listen' AND u.model_id = b.audio_book_id) OR
        (u.ability = 'read' AND u.model_id = b.ebook_id)
-- WHERE 
--    u.user_id = 13042;

;


select * from books where id = 2341;

select * from unlocks where model_id = 714 AND model_type = 'audio_book';

SELECT * FROM books WHERE slug='burhan-urshuu';
SELECT * FROM publishers;
SELECT * FROM authors WHERE name = 'Хайтан';

SELECT * FROM books WHERE author_id = 868;



-- ['Гуравласан аймшиг', 'Анарваан', 'Банхар', 'Хятад сүнс', 'Яс']

SELECT 
    u.user_id,
    u.model_id,
    u.model_type,
    b.title AS book_name,
    b.author_id
FROM 
    unlocks u
LEFT JOIN 
    books b ON 
        (u.model_id = b.audio_book_id AND u.model_type = 'audio_book') OR 
        (u.model_id = b.ebook_id AND u.model_type = 'ebook')
WHERE 
    b.author_id = 868;






SELECT 
    b.title AS book_name,
    COUNT(u.user_id) AS purchase_count
FROM 
    unlocks u
INNER JOIN 
    books b ON 
        (u.model_id = b.audio_book_id AND u.model_type = 'audio_book') OR 
        (u.model_id = b.ebook_id AND u.model_type = 'ebook')
GROUP BY 
    b.title
ORDER BY 
    purchase_count DESC;



SELECT 
    COALESCE(b.title, ab.title, eb.title) AS book_name,
    COUNT(u.user_id) AS purchase_count
FROM 
    unlocks u
LEFT JOIN 
    books b ON 
        (u.model_id = b.audio_book_id AND u.model_type = 'audio_book') OR 
        (u.model_id = b.ebook_id AND u.model_type = 'ebook')
LEFT JOIN 
    audiobooks ab ON u.model_id = ab.id AND u.model_type = 'audio_book'
LEFT JOIN 
    ebooks eb ON u.model_id = eb.id AND u.model_type = 'ebook'
WHERE 
    (b.author_id = 868 OR ab.author_id = 868 OR eb.author_id = 868)
GROUP BY 
    book_name
ORDER BY 
    purchase_count DESC;



SELECT 
    b.title AS book_name,
    COUNT(u.user_id) AS purchase_count
FROM 
    unlocks u
INNER JOIN 
    books b ON 
        (u.model_id = b.audio_book_id AND u.model_type = 'audio_book') OR 
        (u.model_id = b.ebook_id AND u.model_type = 'ebook')
WHERE 
    b.author_id = 868
GROUP BY 
    b.title
ORDER BY 
    purchase_count DESC
LIMIT 50000;


SELECT 
    u.user_id,
    b.title AS book_name,
    COUNT(*) AS purchase_count
FROM 
    unlocks u
INNER JOIN 
    books b ON 
        (u.model_id = b.audio_book_id AND u.model_type = 'audio_book') OR 
        (u.model_id = b.ebook_id AND u.model_type = 'ebook')
WHERE 
    b.author_id = 868
GROUP BY 
    u.user_id, b.title
ORDER BY 
    purchase_count DESC
LIMIT 50000;


SELECT 
    u.user_id,
    COUNT(*) AS purchase_count
FROM 
    unlocks u
INNER JOIN 
    books b ON 
        (u.model_id = b.audio_book_id AND u.model_type = 'audio_book') OR 
        (u.model_id = b.ebook_id AND u.model_type = 'ebook')
WHERE 
    b.author_id = 868
GROUP BY 
    u.user_id
ORDER BY 
    purchase_count DESC
LIMIT 50000;



SELECT 
    u.user_id,
    COUNT(DISTINCT u.model_id) AS unique_purchase_count
FROM 
    unlocks u
INNER JOIN 
    books b ON 
        (u.model_id = b.audio_book_id AND u.model_type = 'audio_book') OR 
        (u.model_id = b.ebook_id AND u.model_type = 'ebook')
WHERE 
    b.author_id = 868
GROUP BY 
    u.user_id
ORDER BY 
    unique_purchase_count DESC
LIMIT 50000;




-- New purchases
SELECT * FROM unlocks LIMIT 500000;

SELECT u.*
FROM unlocks u
JOIN (
  SELECT user_id
  FROM unlocks
  GROUP BY user_id
  HAVING COUNT(*) > 10
) uu ON u.user_id = uu.user_id
LIMIT 500000;

select * from unlocks order by id desc limit 10;
select user_id, model_id from unlocks order by id desc limit 10;
-- model_id is book_id
-- model_type must be audio_book, ebook

select * from books order by id desc limit 10;
-- books has id field which is book_id
-- books has audio_book_id and ebook_id


SELECT DISTINCT u.user_id, b.id AS book_id
FROM unlocks u
JOIN books b ON (u.model_type = 'audio_book' AND u.model_id = b.audio_book_id)
             OR (u.model_type = 'ebook' AND u.model_id = b.ebook_id)
WHERE u.model_type IN ('audio_book', 'ebook')
AND u.user_id IN (
    SELECT user_id
    FROM unlocks
    WHERE model_type IN ('audio_book', 'ebook')
    GROUP BY user_id
    HAVING COUNT(DISTINCT model_id) >= 2
)
ORDER BY u.user_id
LIMIT 500000;









