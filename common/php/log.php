<?php
namespace quartz;
require_once __DIR__ . '/log.php';

class Log {

    static function info($x) {
        echo "<div style='background-color: rgb(200, 220, 240); border: 0px solid darkgrey; color: black; padding: 4px; margin: 4px;'>$x</div>" . PHP_EOL;
    }

    static function debug($x) {
        echo "<div style='background-color: lightgreen; border: 2px solid brightgreen; color: black; font-weight: bold; padding: 4px; margin: 4px;'>$x</div>" . PHP_EOL;
    }

    static function error($x) {
        echo "<div style='background-color: lightyellow; border: 2px solid brightgreen; color: darkred; font-weight: bold; padding: 4px; margin: 4px;'>$x</div>" . PHP_EOL;
    }

    static function except(\Throwable $e) {
        // foreach (preg_split("/\r\n|\n|\r/", $e->getMessage()) as $line) {
        // }
        $msg = $e->getMessage() . PHP_EOL;
        $trace = "";
        foreach ($e->getTrace() as $frame) {
            $file = pathinfo($frame['file'] ?? '', PATHINFO_BASENAME);
            $line = $frame['line'] ?? '';
            $func = ($frame['class'] ?? '') . ($frame['type'] ?? '') . ($frame['function'] ?? '');
            $trace .= ("<li>{$file}({$line}): {$func}</li>" . PHP_EOL);
        }
        Log::error("$msg<ul>$trace</ul>");
    }

}

?>