<?php
namespace books;
require_once __DIR__ . '/../data/genre.php';

// Foreign: 0

class Genre extends model\Genre {
    public $api = null;

    function __construct($name=null, $id=null, $api=null) {
        parent::__construct($name, $id);
        $this->api = $api;
    }

    function add($x) {
        if ($x instanceof Engine) {
            return $x->genres->add($this);
        }
    }

    function remove() {
        $this->api->genres->remove($this);
        $this->id = null;
    }

    function push(?Fields $x=null) {
        return $this->api->genres->set(is_null($x) ? $this : $x);
    }

    function pull(?Fields $x=null) {
        return $this->api->genres->get($x);
    }
}


class GenreManager extends GenreData {
    private $api;
    
    function __construct(\quartz\Database $db, $api) {
        parent::__construct($db);
        $this->api = $api;
    }

    function fetch($x, ?int $id=null, ?bool $debug=false): Genre {
        $x_ = strval($x);
        $g = $this->one($x_);
        if (is_null($g)) {
            $g = new Genre(id:$id, name:$x_, api:$this->api);
            $this->add($g, $debug);
        }
        return $g;
    }

    protected function create($x) {
        return new Genre(id:$x[0], name:$x[1], api:$this->api);
    }
}

?>