<?php
namespace books\model;
require_once __DIR__ . '/../base.php';


class Book extends \books\BookRef {
    public $publisher_id;
    public $title;
    public $year;

    function __construct($publisher_id=null, $title=null, $year=null, $id=null) {
        parent::__construct($id);
        $this->publisher_id = $publisher_id;
        $this->title = $title;
        $this->year = $year;
    }

    public function __toString(): string {
        $ref = parent::__toString();
        $publisher = is_null($this->publisher_id) ? '∅' : $this->publisher_id;
        $title = is_null($this->title) ? '∅' : $this->title;
        $year = is_null($this->year) ? '∅' : $this->year;
        return "book$ref(publisher_id:{$publisher}, title:{$title}, year:{$year})";
    }

    public function copy($x) {
        if ($x instanceof BookRef) {
            parent::copy($x);
            $this->publisher_id = x.publisher_id;
            $this->title = x.title;
            $this->year = x.year;
        }
    }
}

?>