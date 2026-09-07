<?php
namespace books\model;
require_once __DIR__ . '/../base.php';


class Genre extends \books\GenreRef {
    public $name;

    function __construct($name=null, $id=null) {
        parent::__construct($id);
        $this->name = $name;
    }

    public function __toString(): string {
        $ref = parent::__toString();
        $name = is_null($this->name) ? '∅' : $this->name;
        return "genre$ref(name:{$name})";
    }

    public function copy($x) {
        if ($x instanceof GenreRef) {
            parent::copy($x);
            $this->name = x.name;
        }
    }
}

?>