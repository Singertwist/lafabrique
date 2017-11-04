    function init() {
        window.addEventListener('scroll', function(e){
            var distanceY = window.pageYOffset || document.documentElement.scrollTop,
                shrinkOn = 300,
                menuproduits = document.querySelector(".menu-top-commander");
                menupanier = document.querySelector(".fixed-cart");
            if (distanceY > shrinkOn) {
                classie.add(menuproduits,"menu-top-commander-smaller");
                classie.add(menupanier,"fixed-cart-smaller");
            } else {
                if (classie.has(menuproduits,"menu-top-commander-smaller")) {
                    classie.remove(menuproduits,"menu-top-commander-smaller");
                }

                if (classie.has(menupanier,"fixed-cart-smaller")) {
                    classie.remove(menupanier,"fixed-cart-smaller");
                }
            }
        });
    }
    window.onload = init();