   // Back to top button
   $(window).scroll(function () {
    if ($(this).scrollTop() > 300) {
        $('.back-to-top').fadeIn('slow');
    } else {
        $('.back-to-top').fadeOut('slow');
    }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });

    // Fonction pour écrire et effacer le texte
    function writeAndEraseText() {
        var textElement = document.getElementById("dynamic-text");
        var text = "Louez sans stress, avec CAPADATA.";
        var speed = 100; // Vitesse d'écriture en millisecondes
        var eraseSpeed = 50; // Vitesse d'effacement en millisecondes

        // Écrire le texte
        var i = 0;
        var timer = setInterval(function() {
            textElement.innerHTML += text.charAt(i);
            i++;
            if (i > text.length) {
                clearInterval(timer);
                setTimeout(function() {
                    eraseText();
                }, 1000); // Temps avant d'effacer le texte
            }
        }, speed);

        // Effacer le texte
        function eraseText() {
            var timer2 = setInterval(function() {
                var currentText = textElement.innerHTML;
                textElement.innerHTML = currentText.slice(0, -1);
                if (currentText.length === 0) {
                    clearInterval(timer2);
                    setTimeout(function() {
                        writeAndEraseText(); // Répéter le processus
                    }, 1000); // Temps avant de réécrire le texte
                }
            }, eraseSpeed);
        }
    }

    // Appeler la fonction au chargement de la page
    window.onload = function() {
        writeAndEraseText();
    };
