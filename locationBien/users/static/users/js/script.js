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
        var text = "Donnez vie à vos rêves, louez !";
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



/*
<script>
  // Fonction pour écrire et effacer le texte
function writeAndEraseText() {
    var textElement = document.getElementById("dynamic-text");
    var text = "Louez sans stress, avec CAPADATA.";
<!--    var text = "Vivez l'aventure, on s'occupe du reste.";-->
<!--    var text = "Donnez vie à vos rêves, louez !";-->
    var speed = 100; // Vitesse d'écriture en millisecondes
    var eraseSpeed = 50; // Vitesse d'effacement en millisecondes
    var isWriting = false;

    // Écrire le texte
    function writeText() {
        isWriting = true;
        for (var i = 0; i < text.length; i++) {
            (function(i) {
                setTimeout(function() {
                    textElement.innerHTML += text.charAt(i);
                }, i * speed);
            })(i);
        }
        isWriting = false;
        setTimeout(function() {
            eraseText();
        }, text.length * speed); // Temps avant d'effacer le texte
    }

    // Effacer le texte
    function eraseText() {
        if (!isWriting) {
            var timer2 = setInterval(function() {
                var currentText = textElement.innerHTML;
                textElement.innerHTML = currentText.slice(0, -1);
                if (currentText.length === 0) {
                    clearInterval(timer2);
                    setTimeout(function() {
                        writeText(); // Répéter le processus
                    }, 1000); // Temps avant de réécrire le texte
                }
            }, eraseSpeed);
        }
    }

    // Débuter l'écriture du texte
    writeText();
}

// Appeler la fonction au chargement de la page
window.onload = function() {
    writeAndEraseText();
};

    // Appeler la fonction au chargement de la page
    window.onload = function() {
        writeAndEraseText();
    };

</script>*/
