<?php
    $server = 'udungeona.gsmproductions.com';
    $user = '1gamuser_dev';
    $password = '1gameamonth';
    $schema = 'udungeon';

    $server = mysql_connect($server, $user, $password) or die('Erreur Connection DB');
    mysql_select_db($schema,$server);
?>