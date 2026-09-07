<?php
namespace books;
require_once __DIR__ . '/../data/publisher.php';

// Foreign: 0

class Publisher extends model\Publisher {
    public $api = null;

    function __construct($parent_id=null, $name=null, $id=null, $api=null) {
        parent::__construct($parent_id, $name, $id);
        $this->api = $api;
    }

    function add($x) {
        if ($x instanceof Engine) {
            return $x->publishers->add($this);
        }
    }

    function remove() {
        $this->api->publishers->remove($this);
        $this->id = null;
    }

    function push(?Fields $x=null) {
        return $this->api->publishers->set(is_null($x) ? $this : $x);
    }

    function pull(?Fields $x=null) {
        return $this->api->publishers->get($x);
    }
}


class PublisherManager extends PublisherData {
    private $api;
    
    function __construct(\quartz\Database $db, $api) {
        parent::__construct($db);
        $this->api = $api;
    }

    function fetch($x, ?int $id=null, ?bool $debug=false): Publisher {
        $x_ = strval($x);
        $p = $this->one($x_);
        if (is_null($p)) {
            $p = new Publisher(id:$id, name:$x_, api:$this->api);
            $this->add($p, $debug);
        }
        return $p;
    }

    protected function create($x) {
        return new Publisher(id:$x[0], parent_id:$x[1], name:$x[2], api:$this->api);
    }
}

?>