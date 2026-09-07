<?php
namespace books\model;
require_once __DIR__ . '/../base.php';


class Publisher extends \books\PublisherRef {
    public $parent_id;
    public $name;

    function __construct($parent_id=null, $name=null, $id=null) {
        parent::__construct($id);
        $this->parent_id = $parent_id;
        $this->name = $name;
    }

    public function __toString(): string {
        $ref = parent::__toString();
        $parent = is_null($this->parent_id) ? '∅' : $this->parent_id;
        $name = is_null($this->name) ? '∅' : $this->name;
        return "publisher$ref(parent_id:{$parent}, name:{$name})";
    }

    public function copy($x) {
        if ($x instanceof PublisherRef) {
            parent::copy($x);
            $this->parent_id = x.parent_id;
            $this->name = x.name;
        }
    }
}

?>