<?php
$list=$_GET["list"];
// var_dump($_GET);
if ($list=="list"){
    // working on test : http://phpclient.holo.bb0.fr/controller/use_socket_pair.php?command=PP&switchman_id=a1b2c3e4f5g6
    $socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
    socket_connect($socket, '10.10.0.5', 13130);
    socket_write($socket,"list",strlen("list"));
    $buf = socket_read($socket, 1024, PHP_NORMAL_READ);
    // echo("Buffer:".$buf);
    if($buf=="NONE"){
        echo(json_encode(array("NONE")));
    }else{
        $array = explode(";",$buf);
        foreach($array as $key => $value){
            $array[$key]=trim($value);
        }
        echo (json_encode($array));
    }
    
    sleep(1);
    socket_write($socket,"EXIT",strlen("EXIT"));
    socket_close($socket);
}
?>