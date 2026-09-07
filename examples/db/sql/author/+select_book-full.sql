@author/select_all-full
 INNER JOIN `book_author` ba
    ON ba.`author_id` = a.`id`
 INNER JOIN `book` b
    ON b.`id` = ba.`book_id`
 WHERE b.`id` = ?
