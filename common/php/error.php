<?php
namespace quartz;
require_once __DIR__ . '/log.php';
require_once __DIR__ . '/util.php';


enum Error: int {
    case Success         = 0x00;
    case Failed          = 0x01;
    case Invalid         = 0x02;
    case Missing         = 0x03;
    case Overflow        = 0x04;
    case Duplicated      = 0x05;
    case Open            = 0x06;
    case Read            = 0x07;
    case Write           = 0x08;
    case Parsing         = 0x09;
    case Unimplemented   = 0x0A;
    case Exit            = 0xFF;

    static function fail(string $message) {
        throw new \Exception($message);
    }

    static function missing(string $what) {
        Error::fail("Missing: $what");
    }

    static function invalid(string $what, mixed $value) {
        $t = Format::type($value);
        Error::fail("Invalid $what ($t)");
    }

}

?>
