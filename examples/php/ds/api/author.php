<?php
namespace books;
require_once __DIR__ . '/../data/author.php';

// Foreign: 0

class Author extends model\Author {
    public $api = null;

    function __construct($name=null, $id=null, $api=null) {
        parent::__construct($name, $id);
        $this->api = $api;
    }

    function add($x) {
        if ($x instanceof Engine) {
            return $x->authors->add($this);
        }
    }

    function remove() {
        $this->api->authors->remove($this);
        $this->id = null;
    }

    function push(?Fields $x=null) {
        return $this->api->authors->set(is_null($x) ? $this : $x);
    }

    function pull(?Fields $x=null) {
        return $this->api->authors->get($x);
    }
}


class AuthorManager extends AuthorData {
    private $api;
    
    function __construct(\quartz\Database $db, $api) {
        parent::__construct($db);
        $this->api = $api;
    }

    function fetch($x, ?int $id=null, ?bool $debug=false): Author {
        $x_ = strval($x);
        $a = $this->one($x_);
        if (is_null($a)) {
            $a = new Author(id:$id, name:$x_, api:$this->api);
            $this->add($a, $debug);
        }
        return $a;
    }

    protected function create($x) {
        return new Author(id:$x[0], name:$x[1], api:$this->api);
    }
}

?>