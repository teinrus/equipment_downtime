function confirmDeleteDepartment(pk) {
    Swal.fire({
        title: 'Вы уверены?',
        text: 'Вы не сможете восстановить это подразделение!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Удалить',
        cancelButtonText: 'Отмена'
    }).then((result) => {
        if (result.isConfirmed) {
            // Используем fetch для отправки POST-запроса
            fetch(`/settings/department/delete/${pk}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),  // Получаем CSRF токен
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (response.ok) {
                    Swal.fire('Удалено!', 'Подразделение было удалено.', 'success').then(() => {
                        window.location.href = '/settings/departments/';  // Перенаправление на список подразделений
                    });
                } else {
                    Swal.fire('Ошибка!', 'Не удалось удалить подразделение.', 'error');
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
                Swal.fire('Ошибка!', 'Что-то пошло не так.', 'error');
            });
        }
    });
}

function confirmDeleteReason(pk) {
    Swal.fire({
        title: 'Вы уверены?',
        text: 'Вы не сможете восстановить эту причину!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Удалить',
        cancelButtonText: 'Отмена'
    }).then((result) => {
        if (result.isConfirmed) {
            // Используем fetch для отправки POST-запроса на удаление
            fetch(`/settings/downtime_reason/delete/${pk}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),  // Получаем CSRF токен
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (response.ok) {
                    Swal.fire('Удалено!', 'Причина простоя была удалена.', 'success').then(() => {
                        window.location.href = '/settings/reason/';  // Перенаправление на список причин
                    });
                } else {
                    Swal.fire('Ошибка!', 'Не удалось удалить причину простоя.', 'error');
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
                Swal.fire('Ошибка!', 'Что-то пошло не так.', 'error');
            });
        }
    });
}
