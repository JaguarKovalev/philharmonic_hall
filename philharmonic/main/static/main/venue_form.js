document.addEventListener("DOMContentLoaded", function () {
    // Находим элемент select для типа культурного сооружения
    const typeSelect = document.getElementById('id_type');
    const attributesField = document.getElementById('id_specific_attributes');

    // Функция для запроса атрибутов у типа сооружения
    function fetchAttributes(venueTypeId) {
        if (venueTypeId) {
            fetch(`/main/get_venue_attributes/${venueTypeId}/`)
                .then(response => response.json())
                .then(data => {
                    if (attributesField) {
                        // Обновляем поле specific_attributes с новыми атрибутами
                        attributesField.value = JSON.stringify(data.default_attributes, null, 2);
                    }
                });
        }
    }

    // Слушаем изменения в выборе типа
    if (typeSelect) {
        typeSelect.addEventListener('change', function () {
            const selectedType = typeSelect.value;
            fetchAttributes(selectedType);  // Запрашиваем атрибуты для выбранного типа
        });
    }

    // Подгружаем атрибуты при загрузке страницы (если тип уже выбран)
    if (typeSelect && typeSelect.value) {
        fetchAttributes(typeSelect.value);
    }
});
