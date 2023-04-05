<?php
// /**
//  * It returns a string containing a Bootstrap alert.
//  * 
//  * @param text The text you want to display in the alert.
//  * @param color primary, secondary, success, danger, warning, info, light, dark
//  * @param closable true or false
//  * 
//  * @return A string.
//  */
// function alert($text,$color,$closable){
//     $retour=
//     "
//     <div class='alert alert-$color alert-dismissible fade show' role='alert'>
//         <strong>Alerte !</strong> $text";
//     if($closable){
//         $retour.="<button type='button' class='btn-close' data-bs-dismiss='alert' aria-label='Close'></button>";
        
//     }
//     $retour.="</div>";
//     return $retour;
// }
/**
 * It takes an array of column names and an array of rows, and returns a string containing an HTML
 * table.
 * 
 * @param array entete array of strings, each string is a column name
 * @param array content an array of arrays, each array is a row in the table
 * 
 * @return string A string containing the HTML code for a table.
 */
function printTable($entete,$content){
    $tableau="<table class='table text-light'><tr>";
    
    foreach($entete as $nomCol){
        $tableau.="<th>$nomCol</th>";
    }
    $tableau.="</tr>";

    

    foreach($content as $line){
        $tableau.="<tr>";
        foreach($line as $cell){
            $tableau.="<td>$cell</td>";
        }
        $tableau.="</tr>";
    }
    
    
    $tableau.="</table>";
    return $tableau;

}

function gridManager($elementInRow,$elementMax){
    $retourStart="";
    $retourEnd="";
    if($elementInRow==0){
        $retourStart="<div class='row'>";
        $elementInRow++;
    }
    if($elementInRow==$elementMax){
        $retourEnd="</div>";
        $elementInRow=0;
    }else{
        $elementInRow++;
    }
    
    return array($elementInRow,$retourStart,$retourEnd);
}
?>