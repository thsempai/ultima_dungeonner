<?php
    include('header.php');

    $sql =  "select das_data ";
    $sql .= "from data_site ";
    $sql .= "where das_field = 'version'";

    $_SESSION['version'] = 'v?.??';

    $result = mysql_query($sql);
    if ($row = mysql_fetch_array($result))
        {
        $_SESSION['version'] = $row[0]; 
        }

    $sql =  "select das_data ";
    $sql .= "from data_site ";
    $sql .= "where das_field = 'release date'";

    $_SESSION['release_date'] = '??/??/????';
    
    $result = mysql_query($sql);
    if ($row = mysql_fetch_array($result))
        {
        $_SESSION['release_date'] = $row[0]; 
        }

    if(isset($_GET['page']))
        $_SESSION['page']=$_GET['page'];
    else 
        $_SESSION['page']='home'; 
?>

<html>
    <head>
        <title><?php echo $TITLE . ' ' . $_SESSION['version']; ?></title>
        <link href="img/gui/logo.png" rel="icon"/>
        <link rel="stylesheet" href="udungeon.css"/>
    </head>
    <body>

        <h1>
            <?php echo $TITLE . ' ' . $_SESSION['version']; ?>
        </h1>
        <?php
            include('topbar.php');
        

        switch($_SESSION['page'])
            {
            case 'home':        include('home.php');
                                break;
            case 'download':    include('download.php');
                                break;

            case 'music':       include('music.php');
                                break;
            default:            include('home.php');
            }
        ?>

    </body>
</html>
