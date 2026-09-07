@book/select_all-pk
 INNER JOIN `book_author` ba
    ON ba.`book_id` = b.`id`
 INNER JOIN `author` a
    ON a.`id` = ba.`author_id`
 WHERE a .`id` = ?
