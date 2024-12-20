// Функция для получения данных с сервера
async function fetchData() {
    try {
        const response = await fetch('/api/data'); // Запрос к API
        if (!response.ok) {
            throw new Error('Ошибка сети: ' + response.status);
        }
        const data = await response.json(); // Преобразуем JSON в объект
        updateUI(data); // Обновляем интерфейс
    } catch (error) {
        console.error('Ошибка при получении данных:', error);
        alert('Не удалось загрузить данные');
    }
}

// Функция для обновления содержимого страницы
function updateUI(data) {
    const dataList = document.getElementById('dataList');
    dataList.innerHTML = ''; // Очистить старые данные

    data.forEach(item => {
        const listItem = document.createElement('li');
        listItem.textContent = item; // Добавляем текст элемента
        dataList.appendChild(listItem); // Добавляем в список
    });
}

// Обработчик для кнопки
document.getElementById('fetchDataBtn').addEventListener('click', fetchData);