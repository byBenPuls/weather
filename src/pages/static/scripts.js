document.addEventListener('DOMContentLoaded', () => {
    const weatherContainer = document.querySelector('.scrolling-container');
    let isDown = false;
    let startX;
    let scrollLeft;

    weatherContainer.addEventListener('mousedown', (e) => {
        isDown = true;
        startX = e.pageX - weatherContainer.offsetLeft;
        scrollLeft = weatherContainer.scrollLeft;
    });

    document.addEventListener('mouseup', () => {
        isDown = false;
    });

    document.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - weatherContainer.offsetLeft;
        const walk = (x - startX) * 0.85;
        weatherContainer.scrollLeft = scrollLeft - walk;
    });

    weatherContainer.addEventListener('mouseleave', () => {
        const scrollWidth = weatherContainer.scrollWidth;
        const clientWidth = weatherContainer.clientWidth;
        const maxScrollLeft = scrollWidth - clientWidth;
        const currentScrollLeft = weatherContainer.scrollLeft;

        if (currentScrollLeft < 0) {
            weatherContainer.scrollLeft = 0;
        } else if (currentScrollLeft > maxScrollLeft) {
            weatherContainer.scrollLeft = maxScrollLeft;
        }
    });
});
