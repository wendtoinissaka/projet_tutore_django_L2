const signInBtnLink = document.querySelector('.signInBtn-link');
const signUpBtnLink = document.querySelector('.signUpBtn-link');
const wrapper = document.querySelector('.wrapper');

signUpBtnLink.addEventListener('click', () => {
    wrapper.classList.toggle('active');
});

signInBtnLink.addEventListener('click', () => {
    wrapper.classList.toggle('active');
});






function toggleTheme() {
    const body = document.body;
    const sunIcon = document.getElementById('sun-icon');
    const moonIcon = document.getElementById('moon-icon');

    const darkThemeLink = document.getElementById('dark-theme');

    // Toggle la classe pour activer ou désactiver le thème sombre
    body.classList.toggle('dark-theme');

    // Met à jour les couleurs des icônes
    if (body.classList.contains('dark-theme')) {
        sunIcon.style.color = '#000000'; // Couleur du soleil en thème sombre
        moonIcon.style.color = '#ffffff'; // Couleur de la lune en thème sombre
        darkThemeLink.disabled = false; // Activer le thème sombre
    } else {
        sunIcon.style.color = '#ffffff'; // Couleur du soleil en thème clair
        moonIcon.style.color = '#000000'; // Couleur de la lune en thème clair
        darkThemeLink.disabled = true; // Désactiver le thème sombre
    }
}
