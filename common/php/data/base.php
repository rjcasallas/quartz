<?php
namespace quartz;
require_once __DIR__ . '/../error.php';

use PDO;


class Reference {
    public $id;

    public function __construct($id=null) {
        $this->id = $id;
    }

    public function __toString(): string {
        return is_null($this->id) ? '∅' : "⌗{$this->id}";
    }
}


class Database {
    private $db = null;
    private $scheme = null;
    private $queries = null;

    function __construct(string $scheme, ?string $queries=null) {
        $this->queries = new Queries($queries);
        $this->scheme = $scheme;
    }

    function open(string $name, string $user, string $password, string $host='localhost', string $charset='utf8mb4', bool $reset=false){
        // 'mysql:host=localhost;dbname=myapp;charset=utf8mb4',
        $dsn = "mysql:host=$host;dbname=$name;charset=$charset";

        $options = [
            PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES   => false,
        ];
        $this->db = new PDO($dsn, $user, $password, $options);
        if ($reset) {
            $this->create();
        }
    }

    function exec(string $query, array $args=[], bool $debug=false) {
        $sql =  $this->_sql($query, $debug ? $args : null);
        $stmt = $this->db->prepare($sql);
        $stmt->execute($args);
        return $this->db->lastInsertId();
    }

    function begin(string $query, array $args=[], bool $debug=false) {
        $sql =  $this->_sql($query, $debug ? $args : null);
        $cursor = $this->db->prepare($sql);
        $cursor->execute($args);
        return $cursor;
    }

    function next($cursor) {
        if ($cursor instanceof \PDOStatement) {
            return $cursor->fetch(PDO::FETCH_NUM);
        }
        Error::invalid("cursor", $cursor);
    }

    function all(string $query, array $args=[], bool $debug=false) {
        $sql =  $this->_sql($query, $debug ? $args : null);
        $stmt = $this->db->prepare($sql);
        $stmt->execute($args);
        return $stmt->fetchAll(PDO::FETCH_NUM);
    }

    function sql(string $query, bool $debug=false) {
        return $this->_sql($query, $debug ? [] : null);
    }

    private function create() {
        $script = file_get_contents($this->scheme);
        // echo "<br><br>$script<br><br><br>";
        if ($script === false) {
            die("Could not read SQL file");
        }
        $this->db->exec($script);
    }

    function _sql(string $query, ?array $debug=null) {
        $debug_args = is_array($debug) ? implode(', ', $debug) : null;
        if (str_starts_with($query, '@')) {
            $key = substr($query, 1);
            $sql = $this->queries->get($key);
            if (is_string($debug_args)) {
                Log::debug("[$key]<br>$sql<br>[$debug_args]<br>");
            }
            return $sql;
        } elseif (is_string($debug_args)) {
            Log::debug("$query<br>[$debug_args]<br>");
        }
        return $query;
    }
}

?>