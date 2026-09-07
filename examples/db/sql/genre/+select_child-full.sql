@genre/select_all-full
 INNER JOIN `subgenre` sg
    ON sg.`parent_id` = g.`id`
 WHERE sg.`child_id` = ?
