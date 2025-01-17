// Функция для открытия модального окна
function openDowntimeModal(equipmentName) {
    const modal = document.getElementById("downtimeModal");
    const equipmentNameModal = document.getElementById("equipmentNameModal");
    const downtimeTableBody = modal.querySelector("#downtimeTable tbody");
    // Устанавливаем имя оборудования в заголовке
    equipmentNameModal.innerText = equipmentName;
    // Очищаем предыдущие данные в таблице
    downtimeTableBody.innerHTML = '';
    var formModal = document.getElementById('addDowntimeModal');
    formModal.style.display = "none"; // Скрываем форму


    // Запрашиваем данные о простоях
    fetch(`/downtime_details/${equipmentName}/`)
        .then(response => response.json())
        .then(data => {
            if (data.downtimes && data.downtimes.length > 0) {
                data.downtimes.forEach(downtime => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                    <td>${downtime.starttime}</td>
                    <td>${downtime.prostoy}</td>
                    <td data-field="uchastok" class="editable">${downtime.uchastok}</td>
                    <td data-field="otv_pod" class="editable">${downtime.otv_pod}</td>
                    <td data-field="prichina" class="editable">${downtime.prichina}</td>
                    <td data-field="comment" class="editable">${downtime.comment}</td>
                     ${data.is_authenticated ? `
                    <td>
                   
                        <button class="edit-btn">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="save-btn" style="display: none;">
                            <i class="fas fa-save"></i>
                        </button>
                    
                    </td>
` : ''}

                    
                    
                `;
                    downtimeTableBody.appendChild(row);
                    const depId = 0;
                    // Добавляем обработчик событий для кнопок
                    const editBtn = row.querySelector(".edit-btn");
                    const saveBtn = row.querySelector(".save-btn");
                    const editableCells = row.querySelectorAll(".editable");
                    editBtn.addEventListener("click", () => {
                        editableCells.forEach(cell => {
                            
                            const field = cell.getAttribute("data-field");
                    
                            if (!field) {
                                console.error("Атрибут data-field отсутствует у элемента:", cell);
                                return;
                            }
                            const lineId = equipmentName; // Пример: добавьте data-атрибут для строки с ID линии
                            if (field === "uchastok") {
                                const selectSection = document.createElement("select");
                            
                                // Проверяем, что lineId определён
                                if (!lineId) {
                                    console.error("lineId не определён!");
                                    return;
                                }
                            
                                fetch(`settings/get_sections/${lineId}/`)
                                    .then(response => {
                                        if (!response.ok) {
                                            throw new Error(`Ошибка при загрузке: ${response.statusText}`);
                                        }
                                        return response.json();
                                    })
                                    .then(sections => {
                            
                                        // Проверяем, что массив не пустой
                                        if (sections.length === 0) {
                                            console.warn("Нет участков для данной линии.");
                                            const emptyOption = document.createElement("option");
                                            emptyOption.value = "";
                                            emptyOption.textContent = "Нет доступных участков";
                                            selectSection.appendChild(emptyOption);
                                        } else {
                                            sections.forEach(section => {
                                                const opt = document.createElement("option");
                                                opt.value = section.id;
                                                opt.textContent = section.name;
                            
                                                // Устанавливаем выбранный участок
                                                if (cell.innerText.trim() === section.name) {
                                                    opt.selected = true;
                                                }
                            
                                                selectSection.appendChild(opt);
                                            });
                                        }
                                    })
                                    .catch(error => console.error("Ошибка загрузки участков:", error));
                            
                                // Очищаем и заменяем содержимое ячейки
                                cell.innerHTML = ""; // Убедитесь, что ячейка очищена
                                cell.appendChild(selectSection);
                            
                            
                            
                        } else if (field === "otv_pod") {
                                // Выпадающий список для подразделений
                                const selectDept = document.createElement("select");
                                
                                fetch(`/get_departments/`)
                                    .then(response => response.json())
                                    .then(departments => {
                                        departments.forEach(dept => {
                                            const opt = document.createElement("option");
                                            opt.value = dept.id;
                                            opt.textContent = dept.name;
                                            if (cell.innerText === dept.name) {
                                                opt.selected = true;
                                            }
                                            selectDept.appendChild(opt);
                                        });
                                    })
                                    .catch(error => console.error("Ошибка загрузки отделов:", error));
                    
                                cell.innerHTML = "";
                                cell.appendChild(selectDept);
                                
                                // Добавляем событие изменения для загрузки причин
                                selectDept.addEventListener("click", () => {
                                    const deptId = selectDept.value;
                    
                                    // Обновляем причину
                                    const reasonCell = cell.parentElement.querySelector('[data-field="prichina"]');
                                    const selectReason = document.createElement("select");
                                    

                                    fetch(`/api/reasons/${deptId}/`)
                                        .then(response => response.json())
                                        .then(data => {
                                            selectReason.innerHTML = '<option value="">Выберите причину</option>'; // Очистка предыдущих значений
                                           
                                            data.forEach(reason => {
                                                const option = document.createElement('option');
                                                option.value = reason.reason; // Убедитесь, что 'id' правильное
                                                option.textContent = reason.reason; // Убедитесь, что 'reason' правильное
                                                selectReason.appendChild(option);
                                            });
                                        })
                                        .catch(error => console.error("Ошибка загрузки причин:", error));
                    
                                    reasonCell.innerHTML = "";
                                    reasonCell.appendChild(selectReason);
                                });
                            } else if (field === "prichina") {
                                // Причины будут обновляться на основе выбора подразделения
                            } else {
                                // Для остальных полей создаём текстовый ввод
                                const input = document.createElement("input");
                                input.type = "text";
                                input.value = cell.innerText;
                    
                                cell.innerHTML = "";
                                cell.appendChild(input);
                            }
                        });
                    
                        editBtn.style.display = "none";
                        saveBtn.style.display = "inline-block";
                    });
                    
                    
                    
                    
                    
                    saveBtn.addEventListener("click", () => {
                        const updatedData = {};
                    
                        editableCells.forEach(cell => {
                            const field = cell.getAttribute("data-field");
                            if (!field) return;
                    
                            const select = cell.querySelector("select");
                            const input = cell.querySelector("input");
                    
                            if (select) {
                                // Если это выпадающий список
                                updatedData[field] = select.options[select.selectedIndex].text;;
                                cell.innerHTML = select.options[select.selectedIndex].text;;
                            } else if (input) {
                                // Если это текстовое поле
                                const newValue = input.value.trim();
                                updatedData[field] = newValue;
                                cell.innerHTML = newValue;
                            }
                        });
                    
                        // Отправляем данные на сервер
                        fetch(`/update_downtime/${downtime.id}/`, {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                                "X-CSRFToken": getCSRFToken(),
                            },
                            body: JSON.stringify(updatedData),
                        })
                            .then(response => response.json())
                            .then(result => {
                                if (result.success) {
                                    alert("Данные успешно обновлены!");
                                } else {
                                    alert("Ошибка обновления: " + result.error);
                                }
                            })
                            .catch(error => {
                                console.error("Ошибка при обновлении данных:", error);
                            });
                    
                        saveBtn.style.display = "none";
                        editBtn.style.display = "inline-block";
                    });
                    


                });
            } else {
                const row = document.createElement('tr');
                row.innerHTML = `<td colspan="6">Нет данных о простоях</td>`;
                downtimeTableBody.appendChild(row);
            }
        });

    // Отображаем модальное окно
    modal.style.display = "block";
    // Инициализация обработчика события отправки формы, если он еще не установлен
    const addDowntimeForm = document.getElementById("addDowntimeForm");
    if (!addDowntimeForm.onsubmit) {
        addDowntimeForm.onsubmit = function (event) {

            event.preventDefault(); // Предотвращаем отправку формы

            // Получаем значения из формы
            const startTime = document.getElementById("startTime").value; // Поле времени начала
            const endTime = document.getElementById("endTime").value; // Поле времени окончания
            const departmentId = document.getElementById("department").options[document.getElementById("department").selectedIndex].text;
            const uchastokId = document.getElementById("sections").options[document.getElementById("sections").selectedIndex].text;
            const responsibleUnit = document.getElementById("reason").options[document.getElementById("reason").selectedIndex].text;



            const comment = document.getElementById("comment").value;

            // Проверяем, чтобы поля не были пустыми
            if (!startTime || !endTime || !responsibleUnit) {
                alert('Пожалуйста, заполните все обязательные поля.');
                return;
            }



            let name_line = document.getElementById('equipmentNameModal').textContent;


            // Отправляем данные на сервер
            fetch('/add_downtime/', {

                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken() // Получаем CSRF токен
                },


                body: JSON.stringify({
                    line: name_line,
                    start_time: startTime,
                    end_time: endTime,
                    responsible_unit: responsibleUnit,
                    comment: comment,
                    department: departmentId,
                    uchastok: uchastokId,
                })
            })
                .then(response => response.json())
                .then(data => {
                    // Проверка успешности добавления
                    if (data.success) {
                        // Добавляем новую строку в таблицу
                        const row = document.createElement('tr');
                        row.innerHTML = `
                    
                    <td>${startTime}</td>
                    <td>${endTime}</td>
                    <td>${uchastokId}</td>
                    <td>${departmentId}</td>
                    <td>${responsibleUnit}</td>
                    <td>${comment}</td>
                `;
                        downtimeTableBody.appendChild(row);

                        // Очищаем форму
                        addDowntimeForm.reset();
                    } else {
                        alert('Ошибка при добавлении простоя: ' + data.error);
                    }
                })
                .catch(error => {
                    console.error('Ошибка при отправке данных:', error);
                });
        };
    }


}


// Функция для получения CSRF токена
function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Проверяем, начинается ли cookie с 'csrftoken='
            if (cookie.substring(0, "csrftoken=".length) === "csrftoken=") {
                cookieValue = decodeURIComponent(cookie.substring("csrftoken=".length));
                break;
            }
        }
    }
    return cookieValue;
}

// Функция для закрытия модального окна
function closeDowntimeModal() {
    const modal = document.getElementById("downtimeModal");
    modal.style.display = "none";
}

// Закрываем модальное окно при клике за его пределами
window.onclick = function (event) {
    const modal = document.getElementById("downtimeModal");
    if (event.target === modal) {
        closeDowntimeModal();
    }
};

function showFormButton() {
    var formModal = document.getElementById('addDowntimeModal');
    if (formModal.style.display === "none" || formModal.style.display === "") {
        formModal.style.display = "block"; // Показываем форму
    } else {
        formModal.style.display = "none"; // Скрываем форму
    }

};




function confirmDelete(pk) {
    Swal.fire({
        title: 'Вы уверены?',
        text: 'Вы не сможете восстановить эту линию!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Удалить',
        cancelButtonText: 'Отмена'
    }).then((result) => {
        if (result.isConfirmed) {
            // Используем fetch для отправки POST-запроса
            fetch(`/settings/line/delete/${pk}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),  // Получаем CSRF токен
                    'Content-Type': 'application/json'
                }
            })
                .then(response => {
                    if (response.ok) {
                        Swal.fire('Удалено!', 'Линия была удалена.', 'success').then(() => {
                            window.location.href = '/settings/lines/';  // Перенаправление на список настроек
                        });
                    } else {
                        Swal.fire('Ошибка!', 'Не удалось удалить линию.', 'error');
                    }
                })
                .catch(error => {
                    console.error('Ошибка:', error);
                    Swal.fire('Ошибка!', 'Что-то пошло не так.', 'error');
                });
        }
    });
}

// Функция для получения CSRF токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function loadReasons(departmentId) {
    const reasonSelect = document.getElementById('reason');
    reasonSelect.innerHTML = '<option value="">Выберите причину</option>'; // Очистка предыдущих значений

    if (departmentId) {
        fetch(`/api/reasons/${departmentId}/`) // Путь к вашему API для получения причин
            .then(response => response.json())
            .then(data => {
                data.forEach(reason => {
                    const option = document.createElement('option');
                    option.value = reason.id; // Убедитесь, что 'id' правильное
                    option.textContent = reason.reason; // Убедитесь, что 'reason' правильное
                    reasonSelect.appendChild(option);
                });
            })
            .catch(error => {
                console.error('Ошибка:', error);
            });
    }
}


function loadSections(sectionId) {
    const sectionsSelect = document.getElementById('sections');
    sectionsSelect.innerHTML = '<option value="">Выберите участок</option>'; // Очистка предыдущих значений

    if (sectionId) {
        fetch(`/api/section/${sectionId}/`) // Путь к вашему API для получения данных участков
            .then(response => response.json())
            .then(data => {
                data.forEach(section => {
                    const option = document.createElement('option');
                    option.value = section.id; // Используйте 'id' для значения option
                    option.textContent = section.name; // 'name' для текста option
                    sectionsSelect.appendChild(option); // Добавляем option в select
                });
            })
            .catch(error => {
                console.error('Ошибка:', error);
            });
    }
}
