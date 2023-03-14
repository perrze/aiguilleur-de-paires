<?php 
$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
socket_connect($socket, '10.0.0.5', 13130);
socket_write($socket,"1ab2c3d4e5f6",strlen("1ab2c3d4e5f6"));
ob_flush();
socket_write($socket,"list",strlen("list"));
ob_flush();
$buf = socket_read($socket, 1024, PHP_NORMAL_READ);
echo("Buffer:".$buf);
socket_write($socket,"EXIT",strlen("EXIT"));
socket_close($socket);
// echo ("test");
?>

