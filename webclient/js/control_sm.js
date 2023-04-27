function refreshSM() {
    $.ajax({
        type: 'GET',
        url: 'http://api.adp.bb0.fr/switchmans',
        processData: false,
        contentType: false,
        statusCode: {
            200: function (response) {
                // console.log(response);
                option = "<option selected>Choisir l'aiguilleur</option>";
                if (response[0].id == "List Empty") {
                    $("#result").html("Pas d'aiguilleur disponible.");
                    $("#result-div").addClass("border-danger");
                    $("#result-div").removeClass("border-success");

                } else {
                    // console.log(response)
                    $("#result").html("Des aiguilleurs ont été trouvés.")
                    $("#result-div").removeClass("border-danger");
                    $("#result-div").addClass("border-success");
                    for (i = 0; i < response.length; i++) {
                        option += "<option value='" + response[i].id + "'>" + response[i].id + "</option>";
                    }
                }
                $('#select-sm').html(option);
            }
        }

    });

}
function sendCommand(command) {
    var id = $("#select-sm").val();
    var data = { "id": id, "pair": command }
    var delay = 3000; // Prevent bad call
    setTimeout( sendCommand, delay )

    console.log(data);
    $.ajax({
        type: 'POST',
        url: 'http://api.adp.bb0.fr/switchmans/send',
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        statusCode: {
            200: function (response) {
                // console.log(response);
                // console.log("Paire: "+response.pair);
                if ((response.pair)[0] == "P") {
                    $("#result").html("Aiguilleur sur: " + response.pair);
                }
                else {
                    $("#result").html("Aiguilleur en: " + response.pair);
                }
                $("#result-div").removeClass("border-danger");
                $("#result-div").addClass("border-success");
            },
            400: function (xhr) {
                $("#result").html("Erreur, Mauvais formattage JSON");
                $("#result-div").addClass("border-danger");
                $("#result-div").removeClass("border-success");
            },
            404: function (xhr) {
                $("#result").html("Erreur, Mauvais formattage JSON");
                $("#result-div").addClass("border-danger");
                $("#result-div").removeClass("border-success");
            }
        }
    });


}
