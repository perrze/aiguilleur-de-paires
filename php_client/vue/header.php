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
            <img src="/docs/5.2/assets/brand/orange-logo.svg" width="50" height="50" alt="Boosted - Back to Home" loading="lazy">
            </a>
        </div>

        <!-- Burger menu (visible on small screens) -->
        <button class="navbar-toggler collapsed" type="button" data-bs-toggle="collapse" data-bs-target=".global-header-1" aria-controls="global-header-1.1 global-header-1.2" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>

        <!-- Navbar with links -->
        <div id="global-header-1.1" class="navbar-collapse collapse me-lg-auto global-header-1">
            <ul class="navbar-nav">
            <li class="nav-item"><a class="nav-link active" href="#" aria-current="page">Discover</a></li>
            <li class="nav-item"><a class="nav-link" href="#">Shop</a></li>
            </ul>
        </div>

        <!-- Navbar with action icons -->
        <div id="global-header-1.2" class="navbar-collapse collapse d-sm-flex global-header-1">
            <ul class="navbar-nav flex-row">
            <li class="nav-item">
                <a href="#" class="nav-link nav-icon">
                <svg width="1.5rem" height="1.5rem" fill="currentColor" aria-hidden="true" focusable="false" class="overflow-visible">
                    <use xlink:href="/docs/5.2/assets/img/boosted-sprite.svg#search" />
                </svg>
                <span class="visually-hidden">Search</span>
                </a>
            </li>
            <li class="nav-item">
                <a href="#" class="nav-link nav-icon">
                <svg width="1.5rem" height="1.5rem" fill="currentColor" aria-hidden="true" focusable="false" class="overflow-visible">
                    <use xlink:href="/docs/5.2/assets/img/boosted-sprite.svg#buy" />
                </svg>
                <span class="visually-hidden">Basket</span>
                <span class="position-relative align-self-start">
                    <span class="badge bg-info rounded-pill position-absolute top-0 fs-6 text-white translate-middle">
                    1
                    <span class="visually-hidden">shopping basket items</span>
                    </span>
                </span>
                </a>
            </li>
            <li class="nav-item">
                <a href="#" class="nav-link nav-icon">
                <img src="/docs/5.2/assets/img/navbar-contact.png" width="25" height="25" role="img" alt="User" loading="lazy">
                <span class="visually-hidden">My account</span>
                </a>
            </li>
            </ul>
        </div>
        </div>
    </nav>
    </header>


    HTML;

}
?>