<?php

$command=$_GET["command"];
$switchman_id=$_GET["switchman_id"];
// var_dump($_GET);
if (strlen($command)==2 && strlen($switchman_id)==12){
    if(preg_match("/[a-z0-9]{12}/",$switchman_id) && preg_match("/[A-Z]{2}/",$command)){
        // working on test : http://phpclient.holo.bb0.fr/controller/use_socket_pair.php?command=PP&switchman_id=a1b2c3e4f5g6
        $socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
        socket_connect($socket, '10.10.0.5', 13130);
        $output="send ".$switchman_id." ".$command;
        socket_write($socket,$output,strlen($output));

        $buf = socket_read($socket, 1024, PHP_NORMAL_READ);
        // echo("Buffer:".$buf);

        $array = explode(";",$buf);
        foreach($array as $key => $value){
            $array[$key]=trim($value);
        }
        echo (json_encode($array));
        socket_write($socket,"EXIT",strlen("EXIT"));
        sleep(1);
        socket_close($socket);
    }

}


?>