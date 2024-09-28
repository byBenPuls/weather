const background = document.getElementById('background');
const stars = document.getElementById('stars');
const clouds = document.getElementById('clouds');

async function getWeather() {
    try {
        const response = await fetch('http://ваш_бэкенд_адрес/api/weather'); // Замените на адрес вашего бэкенда
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Ошибка при получении данных о погоде:', error);
        return null;
    }
}

function updateBackground(data) {
    if (!data) return;

    const { weather, timeOfDay } = data;
    let themeClass = '';

    if (timeOfDay === 'day') {
        // Дневное время
        stars.style.display = 'none';
        clouds.style.display = 'block';
        if (weather === 'Clear') {
            themeClass = 'fact__theme_day-clear';
        } else if (weather === 'Clouds') {
            themeClass = 'fact__theme_day-cloudy';
        } else if (weather === 'Rain') {
            themeClass = 'fact__theme_day-rain';
        } else if (weather === 'Snow') {
            themeClass = 'fact__theme_day-snow';
        }
    } else {
        // Ночное время
        stars.style.display = 'block';
        clouds.style.display = 'none';
        if (weather === 'Clear') {
            themeClass = 'fact__theme_night-clear';
        } else if (weather === 'Clouds') {
            themeClass = 'fact__theme_night-cloudy';
        } else if (weather === 'Rain') {
            themeClass = 'fact__theme_night-rain';
        } else if (weather === 'Snow') {
            themeClass = 'fact__theme_night-snow';
        }
    }

    background.className = `fact__theme ${themeClass}`;
}

async function main() {
    // const weatherData = await getWeather();
    const weatherData = {weather: "Clear", timeOfDay: "day"}

    updateBackground(weatherData);
}

// Обновляем фон при загрузке страницы
main();

// Обновляем фон каждые 10 минут
setInterval(main, 600000);
