    $(function(){
    $(window).scroll(function(){
        if ($(this).scrollTop() > 300){
            $('.menu-top-commander').addClass('menu-top-commander-smaller');
            $('.fixed-cart').addClass('fixed-cart-smaller');
        }
        else{
            $('.menu-top-commander').removeClass('menu-top-commander-smaller');
            $('.fixed-cart').removeClass('fixed-cart-smaller');
        }
    });
});

/*Ancienne version du fichier avec Bug de Javascript (erreur null). Fonctionne mais génère des messages d'erreur dans la console.*/

/*    function init() {
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
*/