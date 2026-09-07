<?php
namespace quartz;

class Format {

    static function type($x) {
        if (is_object($x)) {
            $c = get_class($x);
            return strval($c);
        }
        $t = gettype($x);
        return strval($t);
    }

    static function string($x) {
        $s = strval($x);
        $t = Format::type($x);
        return "[$t]  $s";
    }

}




?>