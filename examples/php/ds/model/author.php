<?php
namespace books\model;
require_once __DIR__ . '/../base.php';


class Author extends \books\AuthorRef {
    public $name;

    function __construct($name=null, $id=null) {
        parent::__construct($id);
        $this->name = $name;
    }

    public function __toString(): string {
        $ref = parent::__toString();
        $name = is_null($this->name) ? '∅' : $this->name;
        return "author$ref(name:{$name})";
    }

    public function copy($x) {
        if ($x instanceof AuthorRef) {
            parent::copy($x);
            $this->name = x.name;
        }
    }
}

?>