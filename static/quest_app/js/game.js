let gameResetTimer = null;
const RESET_TIMEOUT = 2000; // 2 секунды на возврат

// Функция для сброса игры
async function resetGameOnTabChange() {
    try {
        const csrfToken = getCSRFToken();
        const response = await fetch('/game/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                action: 'reset_game'
            })
        });
        
        console.log('Game reset due to tab change/browser close');
    } catch (error) {
        console.error('Error resetting game:', error);
    }
}

// Функция для обработки видимости страницы
function handleVisibilityChange() {
    if (document.hidden) {
        // Пользователь переключил вкладку или свернул браузер
        console.log('Tab hidden - starting reset timer');
        gameResetTimer = setTimeout(() => {
            resetGameOnTabChange();
        }, RESET_TIMEOUT);
    } else {
        // Пользователь вернулся на вкладку
        console.log('Tab visible - canceling reset timer');
        if (gameResetTimer) {
            clearTimeout(gameResetTimer);
            gameResetTimer = null;
        }
    }
}

// // Функция для обработки закрытия браузера/вкладки
// function handleBeforeUnload(e) {
//     // Сбрасываем игру сразу при попытке закрыть вкладку
//     e.preventDefault();
    
//     // Отправляем синхронный запрос для сброса
//     const xhr = new XMLHttpRequest();
//     xhr.open('POST', '/game/', false); // false для синхронного запроса
//     xhr.setRequestHeader('Content-Type', 'application/json');
//     xhr.setRequestHeader('X-CSRFToken', getCSRFToken());
//     xhr.send(JSON.stringify({
//         action: 'reset_game'
//     }));
    
//     // Стандартное сообщение о закрытии
//     e.returnValue = 'Ваш прогресс будет потерян!';
//     return e.returnValue;
// }

// Инициализация защиты
function initAntiCheatProtection() {
    // Слушаем изменения видимости страницы
    document.addEventListener('visibilitychange', handleVisibilityChange);
    
    // // Слушаем попытки закрытия страницы
    // window.addEventListener('beforeunload', handleBeforeUnload);
    
    // Слушаем уход со страницы
    window.addEventListener('pagehide', resetGameOnTabChange);
    
    // Слушаем потерю фокуса (пользователь переключился на другое окно)
    window.addEventListener('blur', function() {
        console.log('Window lost focus - starting reset timer');
        gameResetTimer = setTimeout(() => {
            resetGameOnTabChange();
        }, RESET_TIMEOUT);
    });
    
    // Слушаем возвращение фокуса
    window.addEventListener('focus', function() {
        console.log('Window gained focus - canceling reset timer');
        if (gameResetTimer) {
            clearTimeout(gameResetTimer);
            gameResetTimer = null;
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('Game script loaded');
    initAntiCheatProtection();
    // Функция для получения CSRF токена
    function getCSRFToken() {
        const hiddenField = document.getElementById('csrf-token');
        if (hiddenField) {
            return hiddenField.value;
        }
        
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue;
    }

        // Запрет копирования текста вопросов
    document.addEventListener('copy', function(e) {
        if (e.target.closest('.puzzle')) {
            e.preventDefault();
            alert('Копирование текста загадок запрещено!');
        }
    });
    
    // Запрет правого клика
    document.addEventListener('contextmenu', function(e) {
        if (e.target.closest('.puzzle')) {
            e.preventDefault();
            alert('Правый клик на загадках запрещен!');
        }
    });
    
    // Запрет выделения текста в загадках
    document.querySelectorAll('.puzzle').forEach(puzzle => {
        puzzle.style.userSelect = 'none';
        puzzle.style.webkitUserSelect = 'none';
    });
    
    // Глобальная переменная для отслеживания текущей музыки
    let currentMusic = null;
    
    // Функция для смены музыки
    function changeRoomMusic(room) {
        console.log('Changing music for room:', room);
        
        // Останавливаем текущую музыку
        if (currentMusic) {
            currentMusic.pause();
            currentMusic.currentTime = 0;
            currentMusic = null;
        }
    
        // Включаем музыку для текущей комнаты
        const roomMusic = document.getElementById(`bg-music-${room}`);
        if (roomMusic) {
            currentMusic = roomMusic;
            roomMusic.volume = 0.3;
        
            // Запускаем только если еще не играет
            if (roomMusic.paused) {
                roomMusic.play().catch(e => {
                    console.log('Автовоспроизведение музыки заблокировано:', e);
                });
            }
        } else {
            console.log(`Музыка для комнаты ${room} не найдена`);
        }
    }

    document.addEventListener('click', function() {
        if (currentMusic && currentMusic.paused) {
            currentMusic.play().catch(e => {
                console.log('Ошибка воспроизведения при клике:', e);
            });
        }
    }, { once: true });
    
    // Воспроизводим музыку текущей комнаты при загрузке
    const currentRoom = '{{ room }}';
    console.log('Current room on load:', currentRoom);
    
    if (currentRoom) {
        changeRoomMusic(currentRoom);
    }

    // Функция для обновления прогресс-бара
    function updateProgressBar(solvedCount) {
        const totalPuzzles = 12;
        const progressPercent = (solvedCount / totalPuzzles) * 100;
        
        const progressFill = document.querySelector('.progress-fill');
        const progressText = document.querySelector('.progress-text');
        const progressBar = document.querySelector('.progress-bar');
        
        if (progressFill) {
            progressFill.style.width = `${progressPercent}%`;
        }

        if (progressText) {
            progressText.textContent = `Прогресс: ${solvedCount}/${totalPuzzles} загадок`;
        }

        // Добавляем класс завершения если все решено
        if (progressBar) {
            if (solvedCount >= totalPuzzles) {
                progressBar.classList.add('completed');
            } else {
                progressBar.classList.remove('completed');
            }
        }
    }


    // Функция для обновления интерфейса комнаты
    function updateRoomInterface(roomData) {
        // Обновляем заголовок комнаты
        const roomTitle = document.querySelector('.room h2');
        if (roomTitle) {
            roomTitle.textContent = roomData.room_name;
        }

        // Обновляем класс комнаты для изображения (если есть изображение)
        const roomImage = document.querySelector('.room-image');
        if (roomImage) {
            roomImage.className = `room-image ${roomData.room}`;
            roomImage.style.backgroundImage = `url('/static/quest_app/img/${roomData.room}.png')`;
        }

        // Обновляем загадки (если есть контейнер)
        const puzzlesContainer = document.querySelector('.puzzles');
        if (puzzlesContainer) {
            if (roomData.puzzles.length === 0) {
                puzzlesContainer.innerHTML = `
                    <div class="welcome-message">
                        <h3>Добро пожаловать в квест!</h3>
                        <p>Выбери комнату для начала приключения. Помни - у тебя есть жизни!</p>
                    </div>
                `;
            } else {
                puzzlesContainer.innerHTML = roomData.puzzles.map(puzzle => `
                    <div class="puzzle" data-difficulty="${puzzle.difficulty}">
                        <h3><i class="fa-solid fa-puzzle-piece fa-pixel fa-blue"></i> Уровень ${puzzle.difficulty}: ${puzzle.name}</h3>
                        <p>${puzzle.description}</p>
                        <form class="puzzle-form ${puzzle.solved ? 'solved' : ''}" data-puzzle-id="${puzzle.id}">
                            <input type="hidden" name="csrfmiddlewaretoken" value="${getCSRFToken()}">
                            <input type="text" name="answer" class="pixel-input" 
                                   placeholder="Твой ответ..." 
                                   ${puzzle.solved ? 'disabled' : ''}>
                            <button type="submit" class="pixel-button" 
                                    ${puzzle.solved ? 'disabled' : ''}>
                                <i class="fa-solid fa-magnifying-glass fa-pixel"></i> Проверить
                            </button>
                        </form>
                        <div class="result-message">
                            ${puzzle.solved ? '✅ Правильно! Загадка решена!' : ''}
                        </div>
                    </div>
                `).join('');
            }
        }

        // Обновляем сердца
        updateHearts(roomData.hearts);

        // Обновляем прогресс-бар
        updateProgressBar(roomData.solved_count);

        // Перепривязываем обработчики событий к новым формам
        bindPuzzleForms();
    }

    // Функция для привязки обработчиков к формам загадок
    function bindPuzzleForms() {
        const puzzleForms = document.querySelectorAll('.puzzle-form');
        
        puzzleForms.forEach(form => {
            form.addEventListener('submit', async function(e) {
                e.preventDefault();
                const formData = new FormData(this);
                const answer = formData.get('answer');
                const puzzleId = this.dataset.puzzleId;
                const resultMessage = this.nextElementSibling;
                        
                // Проверяем, не решена ли уже эта загадка
                if (this.classList.contains('solved')) {
                    resultMessage.textContent = '✅ Эта загадка уже решена!';
                    resultMessage.className = 'result-message success';
                    return;
                }
            
                // Блокируем форму на время запроса
                const input = this.querySelector('input');
                const button = this.querySelector('button');
                input.disabled = true;
                button.disabled = true;
            
                try {
                    const csrfToken = getCSRFToken();
                    const response = await fetch('/game/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrfToken
                        },
                        body: JSON.stringify({
                            action: 'solve_puzzle',
                            puzzle_id: puzzleId,
                            answer: answer
                        })
                    });
                
                    const data = await response.json();
                
                    if (data.success) {
                        const successSound = document.getElementById('success-sound');
                        if (successSound) {
                            successSound.play();
                        }
                        resultMessage.textContent = '✅ Правильно! Загадка решена!';
                        resultMessage.className = 'result-message success';
                        this.classList.add('solved');
                    
                        // Обновляем прогресс-бар
                        if (data.solved_count !== undefined) {
                            updateProgressBar(data.solved_count);
                            
                            // Проверяем победу
                            if (data.solved_count >= 12) {
                                setTimeout(() => {
                                    window.location.href = '/victory/';
                                }, 1000);
                            }
                        } else {
                            // Fallback
                            const currentCount = getCurrentProgress();
                            updateProgressBar(currentCount + 1);
                            if (currentCount + 1 >= 12) {
                                setTimeout(() => {
                                    window.location.href = '/victory/';
                                }, 1000);
                            }
                        }
                    } else {
                        const failSound = document.getElementById('fail-sound');
                        if (failSound) {
                            failSound.play();
                        }
                        if (data.game_over) {
                            window.location.href = '/game-over/';
                        } else {
                            resultMessage.textContent = '❌ Неверно! -1 сердце';
                            resultMessage.className = 'result-message error';
                            
                            // Обновляем сердца
                            if (data.hearts !== undefined) {
                                updateHearts(data.hearts);
                            }
                            
                            // Разблокируем форму для повторной попытки
                            input.disabled = false;
                            button.disabled = false;
                            input.value = '';
                            input.focus();
                        }
                    }
                } catch (error) {
                    console.error('Error:', error);
                    // Разблокируем форму при ошибке
                    input.disabled = false;
                    button.disabled = false;
                }
            });
        });
    }
    
    // Навигация по комнатам
    const roomButtons = document.querySelectorAll('.room-button');
    console.log('Room buttons found:', roomButtons.length);

    roomButtons.forEach(button => {
        button.addEventListener('click', async function(e) {
            e.preventDefault();
            const room = this.dataset.room;
            console.log('Changing room to:', room);

            // Сначала останавливаем всю музыку
            const allBgMusic = document.querySelectorAll('audio[id^="bg-music-"]');
            allBgMusic.forEach(audio => {
                audio.pause();
                audio.currentTime = 0;
            });

            try {
                const csrfToken = getCSRFToken();
                const response = await fetch('/game/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({
                        action: 'change_room',
                        room: room
                    })
                });

                const data = await response.json();
                console.log('Response from server:', data);

                if (data.success) {
                    // Меняем музыку для новой комнаты
                    changeRoomMusic(room);
                    // Обновляем интерфейс без перезагрузки страницы
                    updateRoomInterface(data);
                } else if (data.message) {
                    alert(data.message);
                }
            } catch (error) {
                console.error('Error changing room:', error);
                alert('Ошибка при смене комнаты');
            }
        });
    });
    
    // Обработка кнопки сброса игры
    const resetButton = document.getElementById('reset-button');
    if (resetButton) {
        resetButton.addEventListener('click', async function(e) {
            e.preventDefault();
            if (confirm('Вы уверены, что хотите начать игру заново? Весь прогресс будет потерян.')) {
                try {
                    const csrfToken = getCSRFToken();
                    const response = await fetch('/game/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrfToken
                        },
                        body: JSON.stringify({
                            action: 'reset_game'
                        })
                    });
                    
                    const data = await response.json();
                    if (data.success) {
                        window.location.reload();
                    }
                } catch (error) {
                    console.error('Error:', error);
                }
            }
        });
    }
    
    function updateHearts(hearts) {
        const heartElements = document.querySelectorAll('.fa-heart');
        console.log('Updating hearts to:', hearts, 'Total hearts:', heartElements.length);
        
        heartElements.forEach((heart, index) => {
            if (index < hearts) {
                heart.classList.remove('broken');
                heart.style.opacity = '1';
            } else {
                heart.classList.add('broken');
                heart.style.opacity = '0.3';
            }
        });
    }
    
    function checkVictory() {
        // Проверяем, все ли загадки решены (12 загадок)
        const solvedCount = document.querySelectorAll('.puzzle-form.solved').length;
        if (solvedCount >= 12) {
            window.location.href = '/victory/';
        }
    }
    
    // Инициализация отображения сердец
    const initialHearts = parseInt('{{ player.hearts }}') || 5;
    updateHearts(initialHearts);
    
    // Инициализация прогресс-бара
    const initialSolvedCount = parseInt('{{ player.solved_puzzles|length }}') || 0;
    updateProgressBar(initialSolvedCount);
    
    // Привязываем обработчики к формам при загрузке
    bindPuzzleForms();
    
    // Автовоспроизведение с пользовательским взаимодействием
    document.addEventListener('click', function() {
        if (currentMusic && currentMusic.paused) {
            currentMusic.play().catch(e => console.log('Ошибка воспроизведения:', e));
        }
    }, { once: true });
});

let isMuted = false;
const muteButton = document.getElementById('mute-button');

if (muteButton) {
    muteButton.addEventListener('click', function() {
        isMuted = !isMuted;
        const allAudio = document.querySelectorAll('audio');
        allAudio.forEach(audio => {
            audio.muted = isMuted;
        });
        muteButton.textContent = isMuted ? '🔇' : '🔊';
    });
}