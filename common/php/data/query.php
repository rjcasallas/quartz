<?php
namespace quartz;
require_once __DIR__ . '/../log.php';

class Queries {

    private $queries;

    function __construct($path = null) {
        $this->queries = [];
        $this->load($path);
    }

    function load($path) {
        if ($path !== null && $path !== '' && is_dir($path)) {
            $entries = scandir($path);
            foreach ($entries as $e) {
                if ($e === '.' || $e === '..') continue;
                $full = $path . '/' . $e;
                if (is_dir($full)) {
                    $this->loadDir($full, $e);
                }
            }
        }
        $this->compile();
        // $this->print();
    }

    function get($key) {
        if (array_key_exists($key, $this->queries)) {
            return $this->queries[$key];
        }
        throw new Exception("Missing \"$key\"");
    }

    private function loadDir($dir, $table) {
        $entries = scandir($dir);
        foreach ($entries as $e) {
            $full = $dir . '/' . $e;
            if (is_file($full) && pathinfo($e, PATHINFO_EXTENSION) === 'sql') {
                $base = pathinfo($e, PATHINFO_FILENAME);
                $this->loadSql($full, $table, $base);
            }
        }
    }

    private function loadSql($file, $table, $query) {
        if (str_starts_with($query, '+')) {
            $query = ltrim($query, '+');
        }
        $key = $table . '/' . $query;
        $sql = file_get_contents($file);
        $this->queries[$key] = $sql;
        //echo "$key<br>";
    }

    private function compile() {

        foreach ($this->queries as $key => $sql) {
            $visited = [ $key => true ];
            $this->queries[$key] = $this->refine($sql, $visited);
        }
    }

    private function print() {
        foreach ($this->queries as $key => $sql) {
            Log::debug("[$key]<br>$sql");
        }
    }

    private function refine($sql, $visited) {
        $pattern = '/@([^\s\\\\]+)\\n([\s\S]+)/';
        if (preg_match($pattern, $sql, $m)) {
            $key = $m[1];
            $tail = $m[2];
            if (!array_key_exists($key, $visited) && array_key_exists($key, $this->queries)) {
                $replace = $this->queries[$key];
                $visited[$key] = true;
                return $this->refine($replace . $tail, $visited);
            }
        }
        return $sql;
    }
}

?>