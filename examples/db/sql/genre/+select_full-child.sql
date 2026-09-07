@genre/select_full-all
 INNER JOIN `subgenre` sg
    ON sg.`parent_id` = g.`id`
 WHERE sg.`child_id` = ?
