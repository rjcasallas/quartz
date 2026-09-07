<?php
namespace books;
require_once __DIR__ . '/../data/book.php';

// Foreign: 1

class PublisherSubset {
    private model\Book $book;

    function __construct(model\Book $book) {
        $this->book = $book;
    }

    function get() {
        return is_null($this->book->publisher_id) ? null : $this->book->api->publishers->one($this->_->publisher_id);
    }

    function set(PublisherRef $x) {
        PublisherRef::valid($x);
        $this->book->publisher_id = $x->id;
        $this->api->books->set($x);
    }
}


class Book extends model\Book {
    public $api = null;
    private PublisherSubset $publisher;

    function __construct($publisher_id=null, $title=null, $year=null, $id=null, $api=null) {
        parent::__construct($publisher_id, $title, $year, $id);
        $this->api = $api;
        $this->publisher = new PublisherSubset($this);
    }

    function add($x) {
        if ($x instanceof Engine) {
            return $x->books->add($this);
        }
    }

    function remove() {
        $this->api->books->remove($this);
        $this->id = null;
    }

    function push(?Fields $x=null) {
        return $this->api->books->set(is_null($x) ? $this : $x);
    }

    function pull(?Fields $x=null) {
        return $this->api->books->get($x);
    }
}


class BookManager extends BookData {
    private $api;
    
    function __construct(\quartz\Database $db, $api) {
        parent::__construct($db);
        $this->api = $api;
    }

    function fetch($x, ?int $id=null, ?bool $debug=false): Book {
        $x_ = strval($x);
        $b = $this->one($x_);
        if (is_null($b)) {
            $b = new Book(id:$id, title:$x_, api:$this->api);
            $this->add($b, $debug);
        }
        return $b;
    }

    protected function create($x) {
        return new Book(id:$x[0], publisher_id:$x[1], title:$x[2], year:$x[3], api:$this->api);
    }
}

?>