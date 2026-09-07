@genre/select_pk-all
 INNER JOIN `subgenre` sg
    ON sg.`child_id` = g.`id`
 WHERE sg.`parent_id` = ?
