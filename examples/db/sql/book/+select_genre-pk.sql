@book/select_all-pk
 INNER JOIN `book_genre` bg
    ON bg.`book_id` = b.`id`
 INNER JOIN `genre` g
    ON g.`id` = bg.`genre_id`
 WHERE g.`id` = ?
