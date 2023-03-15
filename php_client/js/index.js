function Sample() {
    var fd = new FormData();
    var email = ""
    var nom = ""
    var prenom = ""
    var apropos = ""
    var poste = ""
    var photo = ""
    console.log("test")
    var email = $("#email_new").val();
    var nom = $("#nom_new").val();
    var prenom = $("#prenom_new").val();
    var apropos = $("#apropos_new").val();
    var poste = $("#poste_new").val();
    var photo = $("#photo_new").attr("src");
    console.log("photo"+photo)

    var files = $('#newPicture')[0].files;

    console.log(files);
    if (files.length > 0) {
        fd.append('newPicture', files[0]);
    }
    fd.append('email', email);
    fd.append('nom', nom);
    fd.append('prenom', prenom);
    fd.append('apropos', apropos);
    fd.append('poste', poste);
    fd.append('photo', photo);
    fd.append('sent', true);
    // console.log(fd["photo"]);
    if (email != "" && nom != "" && prenom != "") {
        // if (true) {
        $.ajax({
            type: 'post',
            url: '/intranet_controleur/users/employes/employe_create.php',
            data: fd,
            dataType: 'text',
            processData: false,
            contentType: false,
            success: function(response) {
                $("#temp").html(response)
                console.log(response);
                var response = JSON.parse(response);
                if (response.status == false) {
                    if (response.infos_lack == false) {
                        $("#create-info").html("Veuillez entrer les informations importantes (email, nom, prenom)");
                        $('#create-info').addClass('text-danger');
                    }

                    if (response.email == false) {
                        $('#create-info').html("email incorrect (x@lepiliermalouin.bzh)");
                        $('#create-info').addClass('text-danger');
                    }
                    if (response.email_exist == false) {
                        $('#create-info').html("L'adresse existe déjà dans la base");
                        $('#create-info').addClass('text-danger');
                    }

                    if (response.nom == false) {
                        $('#create-info').html("Format du nom incorrecte (Retirer les caractères trop spéciaux)");
                        $('#create-info').addClass('text-danger');
                    }
                    if (response.prenom == false) {
                        $('#create-info').html("Format du prenom incorrecte (Retirer les caractères trop spéciaux)");
                        $('#create-info').addClass('text-danger');
                    }
                } else {
                    $('#create-info').html("Utilisateur créer avec succès (id:<strong class='text-danger'>" + response.id + ")</strong>");
                    $('#create-info').removeClass('text-danger');
                    $('#create-info').addClass('text-success');
                    update_list(true);
                    $("#email_new").val("");
                    $("#nom_new").val("");
                    $("#prenom_new").val("");
                    $("#apropos_new").val("");
                    $("#poste_new").val("");
                     
                }
            }
        });

    } else {
        $("#create-info").html("Veuillez entrer les informations importantes (email, nom, prenom)");
        $('#create-info').addClass('text-danger');
    }
    return false;
}
function refreshSM() {


    fd.append('list', list);
    console.log("list");
    // if (true) {
    $.ajax({
        type: 'get',
        url: '/controller/use_socket_list.php',
        data: fd,
        dataType: 'text',
        processData: false,
        contentType: false,
        success: function(response) {
            $("#result").html(response)
            console.log(response);
            var response = JSON.parse(response);
            option="<option selected>Choisir l'aiguilleur</option>";
            for (i=0;i<response.length;i++){
                option+="<option value='"+response[i]+"'>"+response[i]+"</option>";
            }
                    
        }
    });

}