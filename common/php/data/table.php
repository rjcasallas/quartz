<?php
namespace quartz;
require_once __DIR__ . '/base.php';
require_once __DIR__ . '/query.php';

class Info {
    public $table;
    public $values;
    public $replace;

    function __construct(string $table, ?array $values=null, bool $replace=false) {
        $this->table = $table;
        $this->values = is_null($values)? [] : $values;
        $this->replace = $replace;
    }
}

class TagInfo extends Info {
    public $tag;

    function __construct(string $table, string $tag, ?array $values=null, bool $replace=false) {
        parent::__construct($table, $values, $replace);
        $this->tag = $tag;
    }
}

class KeyInfo extends Info {
    public $keys;

    function __construct(string $table, ?array $keys=null, ?array $values=null, bool $replace=false) {
        parent::__construct($table, $values, $replace);
        $this->keys = $keys;
    }
}


abstract class Table {
    public string $name;
    public Database $db;

    function __construct(string $name, Database $db) {
        $this->name = $name;
        $this->db = $db;
    }

    function insert($x, bool $debug=false) {
        $info = ($x instanceof Info) ? $x : $this->_insert($x);
        if ($info instanceof KeyInfo) {
            # INSERT INTO book(title, year) VALUES ('Dune', 1965)
            # REPLACE INTO book(title, year) VALUES ('Dune', 1965)
            $action = $info->replace ? "REPLACE" : "INSERT";
            $columns = array_merge($info->keys, $info->values);
            $names = implode(', ', array_map(fn($c) => "`{$c[0]}`", $columns));
            $args = array_map(fn($c) => $c[1], $columns);
            $marks = array_fill(0, count($columns), '?');
            $query = "{$action} $info->table($names) VALUES($marks)";
            return $this->db->exec($query, $values, $debug);
        }
        elseif ($info instanceof Info) {
            # @book/insert|insert_id|replace
            $args = $info->values;
            if ($info->replace) {
                $query = "@{$info->table}/replace";
            }
            elseif (is_null($info->values[0])) {
                $query = "@{$info->table}/insert";
                array_shift($args);
            }
            else {
                $query = "@{$info->table}/insert_id";
            }
            return $this->db->exec($query, $args, $debug);
        }
        else Error::invalid("insert \"{$this->name}\"", $x);
    }

    function update($x, bool $debug=false) {
        $info = ($x instanceof Info) ? $x : $this->_update($x);
        if ($info instanceof KeyInfo) {
            # UPDATE book SET year=2000 WHERE id=1
            $sets = implode(', ', array_map(fn($c) => "`{$c[0]}`", $info->values));
            $where = implode(' AND ', array_map(fn($c) => "`{$c[0]}`=?", $info->keys));
            $query = "UPDATE `{$info->table}` SET $sets WHERE $where";
            $args = array_merge(array_map(fn($c) => $c[1], $info->values), array_map(fn($c) => $c[1], $info->keys));
            $this->db->exec($query, $args, $debug);
        }
        elseif ($info instanceof Info) {
            # @book/update|replace
            $query = "@{$info->table}/" . ($info->replace ? "replace" : "update");
            $this->db->exec($query, $info->values, $debug);
        }
        else Error::invalid("update \"{$this->name}\"", $x);
        return $x;
    }

    function delete($x, bool $debug=false) {
        $info = ($x instanceof Info) ? $x : $this->_delete($x);
        if ($info instanceof KeyInfo) {
            # DELETE FROM book WHERE year >= ? AND year <= ?
            $query = "DELETE FROM `{$info->table}`";
            $where = [];
            $args = [];
            foreach ($info->keys as $i => $key) {
                if (!is_null($info->keys[$i][1])) {
                    $where[] = "{$info->keys[i][0]}=?";
                    $args[] = $info->keys[i][1];
                }
            }
            if (count($args) > 0) {
                $query .= " WHERE " . implode(' AND ', $where);
            }
            $this->db->exec($query, $args, $debug);
        }
        elseif ($info instanceof TagInfo) {
            $query = "@{$info->table}/delete_{$info->tag}";
            $this->db->exec($query, $info->values, debug);
        }
        else Error::invalid("delete \"{$this->name}\"", $x);
        return $x;
    }

    function deleteAll($debug=false) {
        $this->db->exec("@{$this->table}/delete", [], $debug);
    }

    function begin($x=null, ?string $columns='full', ?array $order=null, ?string $limit=null, bool $debug=false) {
        [$query, $args] = $this->preselect($x, $columns, $order, $limit);
        return $this->db->begin($query, $args, debug:$debug);
    }

    function next($cursor, ?callable $builder=null) {
        $row = $this->db->next($cursor);
        if (is_array($row) && (count($row) > 0)) {
            return is_null($builder) ? $row : $builder($row);
        }
        return null;
    }

    function one($x=null, ?callable $builder=null, ?string $columns='full', ?array $order=null, ?string $limit=null, bool $debug=false) {
        $cur = $this->begin($x, $columns, $order, $limit, $debug);
        return $this->next($cur, $builder);
    }

    function select($x=null, ?callable $builder=null, ?string $columns='full', ?array $order=null, ?string $limit=null, bool $debug=false): array {
        [$query, $args] = $this->preselect($x, $columns, $order, $limit);
        $rows = $this->db->all($query, $args, debug:$debug);
        if (is_array($rows) && (count($rows) > 0)) {
            return is_null($builder) ? $rows :  array_map(fn($r) => $builder($r), $rows);
        }
        return [];
    }

    private function preselect($x=null, ?string $columns='full', ?array $order=null, ?string $limit=null): array {
        $info = ($x instanceof Info) ? $x : $this->_select($x);

        $ord = is_null($order) ? "" : " ORDER BY " . implode(', ', array_map(fn($c) => "`$c`", $order));
        $lim = is_null($limit) ? "" : " LIMIT $lim";
        $tail = $ord . $limit;

        if ($info instanceof KeyInfo) {
            # SELECT id, title FROM book WHERE author = ? AND year > ?
            $nonkeys = implode(', ', array_map(fn($c) => "`{$c[0]}`", $info->values));
            $where = implode(' AND ', array_map(fn($c) => "`{$c[0]}`", $info->keys));
            $args = array_map(fn($c) => $c[1], $info->keys);
            $query = "SELECT $nonkeys FROM `{$info->table}` WHERE {$where}{$tail}";
            return [ $query, $args ];
        }
        elseif ($info instanceof TagInfo) {
            // @book/select_<tag>
            $tag = $info->tag ? $info->tag : 'all';
            $query = $this->db->sql("@{$info->table}/select_$tag-$columns") . $tail;
            return [ $query, $info->values ];
        }
        else Error::invalid("select \"{$this->name}\"", $x);
    }

    abstract public function _insert($x): ?Info;
    abstract public function _update($x): ?Info;
    abstract public function _delete($x): ?Info;
    abstract public function _select($x): ?Info;

}

?>