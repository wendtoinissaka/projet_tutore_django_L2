document.addEventListener('DOMContentLoaded', function() {
    // Liste des messages à afficher
    var messages = ["Bienvenue sur notre site!", "Découvrez nos offres spéciales!", "Contactez-nous pour plus d'informations!"];
    var index = 0;
    var textElement = document.getElementById('texte-dynamique');

    function changeText() {
        textElement.textContent = messages[index];
        index = (index + 1) % messages.length;
    }

    // Démarre l'animation du texte
    setInterval(changeText, 3000); // Change le texte toutes les 3 secondes
});
