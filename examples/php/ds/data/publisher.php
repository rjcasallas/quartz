<?php
namespace books;
require_once __DIR__ . '/../base.php';
require_once __DIR__ . '/../model/publisher.php';
require_once __DIR__ . '/../../common/data/base.php';
require_once __DIR__ . '/../../common/data/table.php';
require_once __DIR__ . '/../../common/error.php';

use quartz\Info, quartz\TagInfo, quartz\KeyInfo;
use quartz\Log;


class PublisherData {
    private \quartz\Table $table;

    function __construct(\quartz\Database $db) {
        $this->table = new PublisherTable("publisher", $db);
    }

    function add($x, bool $debug=false) {
        if (($x instanceof model\Publisher) && is_null($x->id)) {
            $x->id = $this->table->insert($x, $debug);
        }
        elseif (!$this->_replace($x, $debug)) {
            $this->table->insert($x, $debug);
        }
        return $x;
    }

    function push($x, bool $debug=false) {
        if (!$this->_replace($x, $debug)) {
            if (is_array($x) && (x[0] instanceof model\Publisher) && (x[1] instanceof Fields)) {
                // Individual fields
                [$o, $f] = $x;
                if ($f == Fields::Parent) {
                    $x = new KeyInfo("publisher", [ ["id", $o->id] ], [ ["parent_id", $o->parent_id] ]);
                }
                if ($f == Fields::Name) {
                    $x = new KeyInfo("publisher", [ ["id", $o->id] ], [ ["name", $o->name] ]);
                }
            }
            // Update
            return $this->table->update($x, $debug);
        }
    }

    function pull(model\Publisher $x, ?Fields $field=null, bool $debug=false) {
        if (is_null($field)) {
            $row = $this->table->select(KeyInfo("publisher", [ ["id", $x->id] ], [ ["parent_id", $x->parent_id], ["name", $x->name] ]), one:true, debug:$debug);
            $x->parent_id = $row[0];
            $x->name = $row[1];
        }
        elseif (field == Fields::Parent) {
            $x->parent_id = $this->table->select(KeyInfo("publisher", [ ["id", $x->id] ], [ ["parent_id", $x->parent_id] ]), one:true, debug:$debug)[0];
        }
        elseif (field == Fields::Name) {
            $x->name = $this->table->select(KeyInfo("publisher", [ ["id", $x->id] ], [ ["name", $x->name] ]), one:true, debug:$debug)[0];
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
        return false;
    }

    protected function reference($x) {
        return new PublisherRef(id:$x[0]);
    }

    protected function create($x) {
        return new model\Publisher(id:$x[0], parent_id:$x[1], name:$x[2]);
    }
}


class PublisherTable extends \quartz\Table {

    function _insert($x): ?Info {
        // publisher
        if ($x instanceof model\Publisher) {
            return new Info("publisher", [ $x->id, $x->parent_id, $x->name ]);
        }
        return null;
    }

    function _update($x): ?Info {
        // publisher
        if ($x instanceof model\Publisher) {
            return new Info("publisher", [ $x->parent_id, $x->name, $x->id ]);
        }
        return null;
    }

    function _delete($x): ?Info {
        // "parent_publisher" publisher.parent_id → publisher.id (recursive)
        if ($x instanceof ParentPublisherRef) {
            return KeyInfo("publisher", [ ["parent", $x->id] ]);
        }
        // pk
        if (($x instanceof int) || ($x instanceof PublisherRef)) {
            return new TagInfo("publisher", "pk", [ $x->id ]);
        }
        // name
        if ($x instanceof str) {
            return new TagInfo("publisher", "name", [ x ]);
        }
        return null;
    }

    function _select($x=null): ?Info {
        // "parent_publisher" publisher.parent_id → publisher.id (recursive)
        if ($x instanceof ParentPublisherRef) {
            return new TagInfo("publisher", "parent", [ $x->id ]);
        }
        // pk
        if (($x instanceof int) || ($x instanceof PublisherRef)) {
            return new TagInfo("publisher", "pk", [ $x->id ]);
        }
        // name (lookup)
        if ($x instanceof str) {
            return new TagInfo("publisher", "name", [ $x ]);
        }
        // all
        if (is_null($x)) {
            return new TagInfo("publisher", "all");
        }
        return null;
    }
}

?>