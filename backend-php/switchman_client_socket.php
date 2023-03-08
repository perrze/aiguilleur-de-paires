#!/bin/php
<?php
error_reporting(E_ALL);
function read_from_console ($prompt = '') {
    if ( function_exists('readline') ) { 
        $line = trim(readline($prompt));
        if (!empty($line)) {
            readline_add_history($line);
        }
    } else {
        echo $prompt;
        $line = trim(fgets(STDIN));
    }
    return $line;
}


echo "<h2>Connexion TCP/IP</h2>\n";

/* Lit le port du service WWW. */
$service_port = 5000;

/* Lit l'adresse IP du serveur de destination */
$address = "10.0.0.5";

/* Crée un socket TCP/IP. */
$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
if ($socket === false) {
    echo "socket_create() a échoué : raison :  " . socket_strerror(socket_last_error()) . "\n";
} else {
    echo "OK.\n";
}

echo "Essai de connexion à '$address' sur le port '$service_port'...";
$result = socket_connect($socket, $address, $service_port);
if ($socket === false) {
    echo "socket_connect() a échoué : raison : ($result) " . socket_strerror(socket_last_error($socket)) . "\n";
} else {
    echo "OK.\n";
}
// while ($out = socket_read($socket,2048)) {
//     $id=$out;
//     echo("id: ".$id);
// }
$out = socket_read($socket,2048);
$id=$out;
echo("id: ".$id);
  

while(true){
    echo "Entrer une commande (type help for help):\n";
    $order = read_from_console();
    // if($order == "sendusermsg"){
    //     echo("test");
    // }
    // echo("test");
    switch ($order){
        case "help":
            echo("sendusermsg : Envoyer un message de test au switchman\n
            ");
            break;
        case "sendusermsg":
            echo("Entrer votre message:");
            $msg = preg_split('/\s+/', trim(read_from_console()));
            echo ("Entrer l'id de destination:");
            $idTo = preg_split('/\s+/', trim(read_from_console()));
            echo($idTo);
            // A Vérifier: TYPE DE IDTO
            socket_write($socket,"UserMessage",strlen("UserMessage"));
            ob_flush();
            $content=json_encode(array("idFrom"->$id,"idTo"->$idTo,"msg"->$msg));
            socket_write($socket,$content,strlen($content));
            ob_flush();
            break;
    }

}



echo "Lire la réponse : \n\n";




echo "Fermeture du socket...";
socket_close($socket);
echo "OK.\n\n";
?>