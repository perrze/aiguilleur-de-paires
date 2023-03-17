<?php

include_once __DIR__."/../main.php";
/* --------------------------- Controller include --------------------------- */
include_once __DIR__."/functions_vue.php";
require __DIR__."/header.php";

function printCSSImport(){
    /*return "
    <meta charset='utf-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <link href='/css/bootstrap.min.css' rel='stylesheet'>
    <link href='/remixicon/remixicon.css' rel='stylesheet'>
    <link href='/css/surcharge.css' rel='stylesheet'>
    <link rel='stylesheet' href='/css/bootstrap-icons.css'>
    <link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.3/font/bootstrap-icons.css'>

    ";*/
    return "
    <link href='https://cdn.jsdelivr.net' rel='preconnect' crossorigin='anonymous'>
    <link href='https://cdn.jsdelivr.net/npm/boosted@5.2.3/dist/css/boosted.min.css' rel='stylesheet' integrity='sha384-zYFw+mxKy6r9zpAc1NoGiYBfQmxfvg7ONEMr81WeU+WLPPaLC9QTrNGFJTBi3EIn' crossorigin='anonymous'>
    <script src='https://cdn.jsdelivr.net/npm/boosted@5.2.3/dist/js/boosted.bundle.min.js' integrity='sha384-MANW37RG4MpFWPMCcNZBnvSobOkBpIGlbBkEzTtD4FbbOzJXbW8TddND1ak2lfsB' crossorigin='anonymous'></script>
    <link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.3/font/bootstrap-icons.css'>";
}
function printJsImport(){
    
    return "
    <script src='/js/bootstrap.bundle.min.js'></script>
    <script src='/js/jquery-3.6.0.min.js'></script>
    ";
}

function titleDef(){
    global $title;
    $titleFound=true;
    if(!$titleFound){
        $title="Non défini";
    }
    return $title;
}


function printHead(){
    titleDef();
    global $title;
    $htmlTitle="<title>$title</title>";
    $htmlIco="<link rel='icon' type='image/x-icon' href='/sources/logo/PetitLogo.ico'>";
    return printJsImport().printCSSImport().$htmlTitle.$htmlIco;
}
?>