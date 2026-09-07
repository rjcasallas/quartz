<?php
namespace books;
require_once __DIR__ . '/../base.php';
require_once __DIR__ . '/../model/book.php';
require_once __DIR__ . '/../../common/data/base.php';
require_once __DIR__ . '/../../common/data/table.php';
require_once __DIR__ . '/../../common/error.php';

use quartz\Info, quartz\TagInfo, quartz\KeyInfo;
use quartz\Log;


class BookData {
    private \quartz\Table $table;

    function __construct(\quartz\Database $db) {
        $this->table = new BookTable("book", $db);
    }

    function add($x, bool $debug=false) {
        if (($x instanceof model\Book) && is_null($x->id)) {
            $x->id = $this->table->insert($x, $debug);
        }
        elseif (!$this->_replace($x, $debug)) {
            $this->table->insert($x, $debug);
        }
        return $x;
    }

    function push($x, bool $debug=false) {
        if (!$this->_replace($x, $debug)) {
            if (is_array($x) && (x[0] instanceof model\Book) && (x[1] instanceof Fields)) {
                // Individual fields
                [$o, $f] = $x;
                if ($f == Fields::Publisher) {
                    $x = new KeyInfo("book", [ ["id", $o->id] ], [ ["publisher_id", $o->publisher_id] ]);
                }
                if ($f == Fields::Title) {
                    $x = new KeyInfo("book", [ ["id", $o->id] ], [ ["title", $o->title] ]);
                }
                if ($f == Fields::Year) {
                    $x = new KeyInfo("book", [ ["id", $o->id] ], [ ["year", $o->year] ]);
                }
            }
            // Update
            return $this->table->update($x, $debug);
        }
    }

    function pull(model\Book $x, ?Fields $field=null, bool $debug=false) {
        if (is_null($field)) {
            $row = $this->table->select(KeyInfo("book", [ ["id", $x->id] ], [ ["publisher_id", $x->publisher_id], ["title", $x->title], ["year", $x->year] ]), one:true, debug:$debug);
            $x->publisher_id = $row[0];
            $x->title = $row[1];
            $x->year = $row[2];
        }
        elseif (field == Fields::Publisher) {
            $x->publisher_id = $this->table->select(KeyInfo("book", [ ["id", $x->id] ], [ ["publisher_id", $x->publisher_id] ]), one:true, debug:$debug)[0];
        }
        elseif (field == Fields::Title) {
            $x->title = $this->table->select(KeyInfo("book", [ ["id", $x->id] ], [ ["title", $x->title] ]), one:true, debug:$debug)[0];
        }
        elseif (field == Fields::Year) {
            $x->year = $this->table->select(KeyInfo("book", [ ["id", $x->id] ], [ ["year", $x->year] ]), one:true, debug:$debug)[0];
        }
    }
    function remove($x, bool $debug=false) {
        return $this->table->delete($x, $debug);
    }

    function has($x, bool $debug=false): bool {
        return !is_null($this->ref($x, $debug));
    }

    function clear($debug=false) {
        $this->table->deleteAll(debug);
    }

    function refb($x=null, ?array $order=null, ?string $limit=null, bool $debug=false) {
        return $this->table->begin($x, 'pk', $order, $limit, $debug);
    }

    function refn($cursor) {
        return $this->table->next($cursor, $this->reference(...));
    }

    function ref($x=null, ?array $order=null, ?string $limit=null, bool $debug=false) {
        return $this->table->one($x, $this->reference(...), 'pk', $order, $limit, $debug);
    }

    function refs($x=null, ?array $order=null, ?string $limit=null, bool $debug=false): array {
        return $this->table->select($x, $this->reference(...), 'pk', $order, $limit, $debug);
    }

    function begin($x=null, ?string $columns='full', ?array $order=null, ?string $limit=null, bool $debug=false) {
        return $this->table->begin($x, $columns, $order, $limit, $debug);
    }

    function next($cursor, ?callable $builder=null) {
        $fn = is_null($builder) ? $this->create(...) : $builder;
        return $this->table->next($cursor, $fn);
    }

    function one($x=null, ?callable $builder=null, ?string $columns='full', ?array $order=null, ?string $limit=null, bool $debug=false) {
        $fn = is_null($builder) ? $this->create(...) : $builder;
        return $this->table->one($x, $fn, $columns, $order, $limit, $debug);
    }

    function all($x=null, ?callable $builder=null, ?string $columns='full', ?array $order=null, ?string $limit=null, bool $debug=false): array {
        $fn = is_null($builder) ? $this->create(...) : $builder;
        return $this->table->select($x, $fn, $columns, $order, $limit, $debug);
    }

    protected function _replace($x, bool $allow_delete=false, bool $debug=false) {
        // "book_author" author.id → book.id
        if ($x instanceof BookAuthorRef) {
            if ($x->book_id && $x->author_id) {
                return $this->table->update($x, $debug);
            }
            elseif ($allow_delete) {
                return $this->table->delete($x, $debug);
            }
            else {
                \quartz\Error::invalid('"book_author" replace', $x);
            }
        }
        // "book_genre" genre.id → book.id
        if ($x instanceof BookGenreRef) {
            if ($x->book_id && $x->genre_id) {
                return $this->table->update($x, $debug);
            }
            elseif ($allow_delete) {
                return $this->table->delete($x, $debug);
            }
            else {
                \quartz\Error::invalid('"book_genre" replace', $x);
            }
        }
        return false;
    }

    protected function reference($x) {
        return new BookRef(id:$x[0]);
    }

    protected function create($x) {
        return new model\Book(id:$x[0], publisher_id:$x[1], title:$x[2], year:$x[3]);
    }
}


class BookTable extends \quartz\Table {

    function _insert($x): ?Info {
        // book
        if ($x instanceof model\Book) {
            return new Info("book", [ $x->id, $x->publisher_id, $x->title, $x->year ]);
        }
        return null;
    }

    function _update($x): ?Info {
        // book
        if ($x instanceof model\Book) {
            return new Info("book", [ $x->publisher_id, $x->title, $x->year, $x->id ]);
        }
        // "book_author" author.id → book.id
        if ($x instanceof BookAuthor) {
            return new Info("book_author", [$x->rank, $x->book_id, $x->author_id ], true);
        }
        // "book_genre" genre.id → book.id
        if ($x instanceof BookGenreRef) {
            return new Info("book_genre", [$x->book_id, $x->genre_id ], true);
        }
        return null;
    }

    function _delete($x): ?Info {
        // "book_author" author.id → book.id
        if ($x instanceof BookAuthorRef) {
            return KeyInfo("book_author", [ ["book_id", $x->book_id], ["author_id", $x->author_id] ]);
        }
        // "book_genre" genre.id → book.id
        if ($x instanceof BookGenreRef) {
            return KeyInfo("book_genre", [ ["book_id", $x->book_id], ["genre_id", $x->genre_id] ]);
        }
        // pk
        if (($x instanceof int) || ($x instanceof BookRef)) {
            return new TagInfo("book", "pk", [ $x->id ]);
        }
        // title
        if ($x instanceof str) {
            return new TagInfo("book", "title", [ x ]);
        }
        return null;
    }

    function _select($x=null): ?Info {
        // "book_author" author.id → book.id
        if ($x instanceof AuthorRef) {
            return new TagInfo("book", "author", [ $x->id ]);
        }
        // "book_genre" genre.id → book.id
        if ($x instanceof GenreRef) {
            return new TagInfo("book", "genre", [ $x->id ]);
        }
        // pk
        if (($x instanceof int) || ($x instanceof BookRef)) {
            return new TagInfo("book", "pk", [ $x->id ]);
        }
        // title (lookup)
        if ($x instanceof str) {
            return new TagInfo("book", "title", [ $x ]);
        }
        // publisher (foreign)
        if ($x instanceof PublisherRef) {
            return new TagInfo("book", "publisher", [ $x->id ]);
        }
        // all
        if (is_null($x)) {
            return new TagInfo("book", "all");
        }
        return null;
    }
}

?>