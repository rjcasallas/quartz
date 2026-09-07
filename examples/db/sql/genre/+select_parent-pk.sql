@genre/select_all-pk
 INNER JOIN `subgenre` sg
    ON sg.`child_id` = g.`id`
 WHERE sg.`parent_id` = ?
