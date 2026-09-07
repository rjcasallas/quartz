<?php
namespace books;
require_once __DIR__ . '/common/base.php';
require_once __DIR__ . '/data/author.php';
require_once __DIR__ . '/data/book.php';
require_once __DIR__ . '/data/genre.php';
require_once __DIR__ . '/data/publisher.php';


class Dataset {
    public $db = null;
    public $authors = null;
    public $books = null;
    public $genres = null;
    public $publishers = null;

    function __construct(string $scheme, ?string $queries=null) {
        $this->db = new quartz\Database($scheme, $queries);
        $this->authors = new AuthorData($this->db);
        $this->books = new BookData($this->db);
        $this->genres = new GenreData($this->db);
        $this->publishers = new PublisherData($this->db);
    }

    function open(bool $reset=false) {
        $this->db->open(getenv('DB_NAME'), getenv('DB_USER'), getenv('DB_PASS'), reset:$reset);
    }

    function isOpen(): bool {
        return $this->db.isOpen();
    }
}


?>