<?php
function printHeader(){
    $header=
    <<<HTML
    <header>
    <nav class="navbar navbar-dark bg-dark navbar-expand-lg" aria-label="Global navigation - Standard example">
        <div class="container-xxl">

        <!-- Orange brand logo -->
        <div class="navbar-brand me-auto me-lg-4">
            <a class="stretched-link" href="#">
            <img src="/sources/brand/orange-logo.svg" width="50" height="50" alt="Boosted - Back to Home" loading="lazy">
            </a>
            <h1 class="two-lined">
            Orange
            <br>
            UI NC - EQ MA LHA
            </h1>
        </div>

    
        </div>
    </nav>
    </header>


    HTML;
    return $header;

}
?>