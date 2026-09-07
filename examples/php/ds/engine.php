<?php
namespace books;
require_once __DIR__ . '/../common/data/base.php';
require_once __DIR__ . '/api/author.php';
require_once __DIR__ . '/api/book.php';
require_once __DIR__ . '/api/genre.php';
require_once __DIR__ . '/api/publisher.php';


class Engine {
    public $db = null;
    public $authors = null;
    public $books = null;
    public $genres = null;
    public $publishers = null;

    function __construct(string $scheme, ?string $queries=null) {
        $this->db = new \quartz\Database($scheme, $queries);
        $this->authors = new AuthorManager($this->db, $this);
        $this->books = new BookManager($this->db, $this);
        $this->genres = new GenreManager($this->db, $this);
        $this->publishers = new PublisherManager($this->db, $this);
    }

    function open(bool $reset=false) {
        $this->db->open(getenv('DB_NAME'), getenv('DB_USER'), getenv('DB_PASS'), reset:$reset);
    }
}

?>