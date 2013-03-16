<?php
    $server = '1gamdb.gsmproductions.com';
    $user = '1gamuser_dev';
    $password = '1gameamonth';
    $schema = '1gam201302';

    $server = mysql_connect($server, $user, $password) or die('Erreur Connection DB');
    mysql_select_db($schema,$server);

    $sql =  "select das_data ";
    $sql .= "from data_site ";
    $sql .= "where das_field = 'version'";

    $version = 'v?.??';

    $result = mysql_query($sql);
    if ($row = mysql_fetch_array($result))
        {
        $version = $row[0]; 
        }

    $sql =  "select das_data ";
    $sql .= "from data_site ";
    $sql .= "where das_field = 'release date'";

    $release_date = '??/??/????';
    
    $result = mysql_query($sql);
    if ($row = mysql_fetch_array($result))
        {
        $release_date = $row[0]; 
        }
?>

<html>
    <head>
        <title>Ultima Dungeonner <?php echo $version; ?></title>
        <link rel="stylesheet" href="udungeon.css"/>
    </head>
    <body>

        <h1>
            Utilma Dungeonner <?php echo $version; ?>
        </h1>

        <div class="screenshot">
            <img src="screenshots/image.png" alt="Ultima dungeonner">
        </div>
            
        <div class="date_release">
            Release update : <?php echo $release_date; ?>
        </div>

    </body>
</html>