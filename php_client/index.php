
<!DOCTYPE html>
<?php require_once __DIR__."/main.php"; ?> 
<html>

<head>
    <?php include_once __DIR__."/vue/head.php"; ?>
    <?php echo printHead(); ?>
</head>

<body>
    <div class="bg-dark text-light text-center">
            <h1>Intranet du Pilier Malouin !</h1>
    </div>
    <main>
    <script src="/js/index.js"></script>
        
        <div class="container">

            <div class="row">
                <h2 class="text-center text-warning">Veuillez vous connecter pour accéder à l'intranet</h2>
                <div class="col-sm-4"></div>
                <div class="col-sm-4">

                    <div>

                        <label for="identity" class="text-light">Veuillez entrer votre identifiant (Mail ou ID)</label>
                        <span id='identity-info' class='info'></span><br>
                        <div class="form-floating">
                            <input id="identity" placeholder="" name="identity" type="text" class="form-control">
                            <label for="identity">x@lepiliermalouin.bzh ou AAXXXX</label>
                        </div>
                        <i class="bi-alarm" style="font-size: 2rem; color: cornflowerblue;"></i>

                        <label for="password" class="text-light">Veuillez entrer votre mot de passe</label>
                        <span id='password-info' class='info'></span><br>
                        <div class="form-floating">
                            <input id="password" placeholder="" name="password" type="password" class="form-control">
                            <label for="password">Mot de passe</label>
                        </div>
                        <button class="btn btn-info" onclick='do_login(true)'>Se connecter</button>
                        <span id='connected-info' class='info'></span><br>
                        <p ><a href="/register.php" class="text-primary">S'inscrire</a></p>
                    </div>
                </div>
            </div>
        </div>
    </main>


</body>

</html>