
<!DOCTYPE html>
<?php require_once __DIR__."/main.php"; ?> 
<html>

<head>
    <?php include_once __DIR__."/vue/head.php"; ?>
    <?php echo printHead(); ?>
</head>

<body>
    <?php echo printHeader(); ?>
    <main>
    <!-- <script src="/js/index.js"> -->
        <script>
function refreshSM() {

    // console.log("list");
    // if (true) {
    $.ajax({
        type: 'GET',
        url: '/controller/use_socket_list.php',
        data: "list=list",
        dataType: 'text',
        processData: false,
        contentType: false,
        success: function(response) {
            
            console.log(response);
            var response = JSON.parse(response);
            option="<option selected>Choisir l'aiguilleur</option>";
            if(response[0]=="NONE"){
                $("#result").html("Pas d'aiguilleurs disponible");
                $("#result-div").addClass("border-danger");
                $("#result-div").removeClass("border-success");
            }else{
                $("#result").html(response)
                $("#result-div").removeClass("border-danger");
                $("#result-div").addClass("border-success");
                for (i=0;i<response.length;i++){
                    option+="<option value='"+response[i]+"'>"+response[i]+"</option>";
                }
                $('#select-sm').html(option);

            }
            
            console.log(option)
                    
        }
    });

}
function sendCommand(command){
    var fd = new FormData();
    var id = "";
    var id = $("#select-sm").val();
    fd.append("command",command);
    fd.append("switchman_id",id)

    var getRequest="switchman_id="+id+"&command="+command;

    console.log(getRequest);
    // console.log(fd);
    $.ajax({
            type: 'GET',
            url: '/controller/use_socket_pair.php',
            data: getRequest,
            dataType: 'text',
            processData: false,
            contentType: false,
            success: function(response) {
                var response = JSON.parse(response);
                console.log(response);
                if(response[0]=="OK"){
                    if(response[1][0]=="P"){
                        $("#result").html("Résultat : Aiguilleur sur: "+response[1]);
                    }
                    else{
                        $("#result").html("Résultat : Aiguilleur en: "+response[1]);
                    }
                    $("#result-div").removeClass("border-danger");
                    $("#result-div").addClass("border-success");
                }else{
                    $("#result").html("Résultat : Erreur");
                    $("#result-div").addClass("border-danger");
                    $("#result-div").removeClass("border-success");
                }
                // $("#result").html(response)
                // console.log(response);
            }
        });


}

    </script>
        
        <div class="container my-4">
            <h2 class="my-4">Contrôler vos aiguilleurs</h2>
            <div id="forms mx-2">
                <div id="select-sm-div" class="row">
                   <div class="col-lg-9">
                        <select id="select-sm" class="form-select" aria-label="Select Switchman">
                            <option>Choisir l'aiguilleur</option>
                        </select>
                    </div>
                    <div class="col-lg-3">
                        <button type="submit" class="btn btn-primary mb-3 col form-control" onclick="refreshSM()">Actualiser</button>
                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-3">
                        <button id="P1" onclick="sendCommand('P1')" type="submit" class="btn btn-secondary mb-3 col form-control">Paire 1</button>
                    </div>
                    <div class="col-lg-3">
                        <button id="P2" onclick="sendCommand('P2')" type="submit" class="btn btn-success mb-3 col form-control">Paire 2</button>
                    </div>
                    <div class="col-lg-3">
                        <button id="P3" onclick="sendCommand('P3')" type="submit" class="btn btn-danger mb-3 col form-control">Paire 3</button>
                    </div>
                    <div class="col-lg-3">
                        <button id="P4" onclick="sendCommand('P4')" type="submit" class="btn btn-info mb-3 col form-control">Paire 4</button>
                    </div>
                </div>
                <div class="row">
                    <div class="col">
                        <button id="CC" onclick="sendCommand('CC')" type="submit" class="btn btn-primary mb-3 col form-control">Boucle</button>
                    </div>
                    <div class="col">
                        <button id="BO" onclick="sendCommand('BO')" type="submit" class="btn btn-primary mb-3 col form-control">Ouvert</button>
                    </div>
                </div>
                <div id="result-div" class="container border">
                        <p id="result" class="p-1 mx-1"></p>
                </div>
            </div>
        </div>
    </main>


</body>

</html>