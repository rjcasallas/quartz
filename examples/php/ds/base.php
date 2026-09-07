<?php
namespace books;
require_once __DIR__ . '/../common/data/base.php';

#
# Fields (10)
#

enum Fields {
    case Author;
    case Book;
    case Child;
    case Genre;
    case Name;
    case Parent;
    case Publisher;
    case Rank;
    case Title;
    case Year;
}

#
# Entities (4)
#

class AuthorRef extends \quartz\Reference {

    public static function valid($x, $nullable=false) {
        if ($nullable && is_null($x)) {
            return null;
        }
        elseif (is_int($x)) {
            return $x;
        }
        elseif ($x instanceof AuthorRef) {
            return $x;
        }
        throw new Exception("Invalid author reference: $x");
    }
}


class BookRef extends \quartz\Reference {

    public static function valid($x, $nullable=false) {
        if ($nullable && is_null($x)) {
            return null;
        }
        elseif (is_int($x)) {
            return $x;
        }
        elseif ($x instanceof BookRef) {
            return $x;
        }
        throw new Exception("Invalid book reference: $x");
    }
}


class GenreRef extends \quartz\Reference {

    public static function valid($x, $nullable=false) {
        if ($nullable && is_null($x)) {
            return null;
        }
        elseif (is_int($x)) {
            return $x;
        }
        elseif ($x instanceof GenreRef) {
            return $x;
        }
        throw new Exception("Invalid genre reference: $x");
    }
}


class PublisherRef extends \quartz\Reference {

    public static function valid($x, $nullable=false) {
        if ($nullable && is_null($x)) {
            return null;
        }
        elseif (is_int($x)) {
            return $x;
        }
        elseif ($x instanceof PublisherRef) {
            return $x;
        }
        throw new Exception("Invalid publisher reference: $x");
    }
}

#
# Junctions (3)
#

class BookAuthorRef {
    public $book_id;
    public $author_id;

    public function __construct($book_id=null, $author_id=null) {
        $this->book_id = $book_id;
        $this->author_id = $author_id;
    }

    public function __toString(): string {
        $book = is_null($this->book_id) ? '∅' : $this->book_id;
        $author = is_null($this->author_id) ? '∅' : $this->author_id;
        return "book_author⌗{$book}⌗{$author}";
    }
}


class BookAuthor extends BookAuthorRef {
    public $rank;

    public function __construct($book_id=null, $author_id=null, $rank=null) {
        parent::__construct($book_id, $author_id);
        $this->rank = $rank;
    }

    public function __toString(): string {
        $ref = parent::__toString();
        $rank = is_null($this->rank) ? '∅' : $this->rank;
        return "$ref(rank:{$rank})";
    }

    public function copy($x) {
        if ($x instanceof BookAuthorRef) {
            parent::copy($x);
            $this->rank = x.rank;
        }
    }
}


class BookGenreRef {
    public $book_id;
    public $genre_id;

    public function __construct($book_id=null, $genre_id=null) {
        $this->book_id = $book_id;
        $this->genre_id = $genre_id;
    }

    public function __toString(): string {
        $book = is_null($this->book_id) ? '∅' : $this->book_id;
        $genre = is_null($this->genre_id) ? '∅' : $this->genre_id;
        return "book_genre⌗{$book}⌗{$genre}";
    }
}


class SubgenreRef {
    public $parent_id;
    public $child_id;

    public function __construct($parent_id=null, $child_id=null) {
        $this->parent_id = $parent_id;
        $this->child_id = $child_id;
    }

    public function __toString(): string {
        $parent = is_null($this->parent_id) ? '∅' : $this->parent_id;
        $child = is_null($this->child_id) ? '∅' : $this->child_id;
        return "subgenre⌗{$parent}⌗{$child}";
    }
}

#
# Self-referencing (3)
#

# "child_genre" genre.id → genre.id
class ChildGenreRef extends GenreRef {

}

# "parent_genre" genre.id → genre.id
class ParentGenreRef extends GenreRef {

}

# "parent_publisher" publisher.parent_id → publisher.id
class ParentPublisherRef extends PublisherRef {

}


?>