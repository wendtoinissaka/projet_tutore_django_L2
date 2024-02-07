<script>
    const scrollingText = document.getElementById('scrolling-text');
    const slogans = ['Slogan 1', 'Slogan 2', 'Slogan 3']; // Ajoutez vos slogans ici
    let currentIndex = 0;

    function scrollSlogan() {
        if (currentIndex === slogans.length) {
            currentIndex = 0;
        }
        const currentSlogan = slogans[currentIndex];
        let index = 0;
        const interval = setInterval(() => {
            if (index === currentSlogan.length + 1) {
                clearInterval(interval);
                setTimeout(() => {
                    eraseSlogan(currentSlogan);
                }, 1000);
            } else {
                scrollingText.textContent = currentSlogan.slice(0, index);
                index++;
            }
        }, 100);
        currentIndex++;
    }

    function eraseSlogan(slogan) {
        let index = slogan.length;
        const interval = setInterval(() => {
            if (index === 0) {
                clearInterval(interval);
                setTimeout(() => {
                    scrollSlogan();
                }, 1000);
            } else {
                scrollingText.textContent = slogan.slice(0, index);
                index--;
            }
        }, 100);
    }

    scrollSlogan();
</script>
