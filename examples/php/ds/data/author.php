<?php
namespace books;
require_once __DIR__ . '/../base.php';
require_once __DIR__ . '/../model/author.php';
require_once __DIR__ . '/../../common/data/base.php';
require_once __DIR__ . '/../../common/data/table.php';
require_once __DIR__ . '/../../common/error.php';

use quartz\Info, quartz\TagInfo, quartz\KeyInfo;
use quartz\Log;


class AuthorData {
    private \quartz\Table $table;

    function __construct(\quartz\Database $db) {
        $this->table = new AuthorTable("author", $db);
    }

    function add($x, bool $debug=false) {
        if (($x instanceof model\Author) && is_null($x->id)) {
            $x->id = $this->table->insert($x, $debug);
        }
        elseif (!$this->_replace($x, $debug)) {
            $this->table->insert($x, $debug);
        }
        return $x;
    }

    function push($x, bool $debug=false) {
        if (!$this->_replace($x, $debug)) {
            if (is_array($x) && (x[0] instanceof model\Author) && (x[1] instanceof Fields)) {
                // Individual fields
                [$o, $f] = $x;
                if ($f == Fields::Name) {
                    $x = new KeyInfo("author", [ ["id", $o->id] ], [ ["name", $o->name] ]);
                }
            }
            // Update
            return $this->table->update($x, $debug);
        }
    }

    function pull(model\Author $x, ?Fields $field=null, bool $debug=false) {
        if (is_null($field)) {
            $row = $this->table->select(KeyInfo("author", [ ["id", $x->id] ], [ ["name", $x->name] ]), one:true, debug:$debug);
            $x->name = $row[0];
        }
        elseif (field == Fields::Name) {
            $x->name = $this->table->select(KeyInfo("author", [ ["id", $x->id] ], [ ["name", $x->name] ]), one:true, debug:$debug)[0];
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
        // "author_book" book.id → author.id
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
        return false;
    }

    protected function reference($x) {
        return new AuthorRef(id:$x[0]);
    }

    protected function create($x) {
        return new model\Author(id:$x[0], name:$x[1]);
    }
}


class AuthorTable extends \quartz\Table {

    function _insert($x): ?Info {
        // author
        if ($x instanceof model\Author) {
            return new Info("author", [ $x->id, $x->name ]);
        }
        return null;
    }

    function _update($x): ?Info {
        // author
        if ($x instanceof model\Author) {
            return new Info("author", [ $x->name, $x->id ]);
        }
        // "author_book" book.id → author.id
        if ($x instanceof BookAuthor) {
            return new Info("book_author", [$x->rank, $x->book_id, $x->author_id ], true);
        }
        return null;
    }

    function _delete($x): ?Info {
        // "author_book" book.id → author.id
        if ($x instanceof BookAuthorRef) {
            return KeyInfo("book_author", [ ["book_id", $x->book_id], ["author_id", $x->author_id] ]);
        }
        // pk
        if (($x instanceof int) || ($x instanceof AuthorRef)) {
            return new TagInfo("author", "pk", [ $x->id ]);
        }
        // name
        if ($x instanceof str) {
            return new TagInfo("author", "name", [ x ]);
        }
        return null;
    }

    function _select($x=null): ?Info {
        // "author_book" book.id → author.id
        if ($x instanceof BookRef) {
            return new TagInfo("author", "book", [ $x->id ]);
        }
        // pk
        if (($x instanceof int) || ($x instanceof AuthorRef)) {
            return new TagInfo("author", "pk", [ $x->id ]);
        }
        // name (lookup)
        if ($x instanceof str) {
            return new TagInfo("author", "name", [ $x ]);
        }
        // all
        if (is_null($x)) {
            return new TagInfo("author", "all");
        }
        return null;
    }
}

?>