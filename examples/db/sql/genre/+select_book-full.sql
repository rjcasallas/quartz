@genre/select_all-full
 INNER JOIN `book_genre` bg
    ON bg.`genre_id` = g.`id`
 INNER JOIN `book` b
    ON b.`id` = bg.`book_id`
 WHERE b.`id` = ?
