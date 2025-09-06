document.addEventListener('DOMContentLoaded', function() {
    console.log('Game script loaded');
    
    // Функция для получения CSRF токена
    function getCSRFToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue;
    }
    
    // Функция для смены музыки
    function changeRoomMusic(room) {
        // Останавливаем все музыки
        const allMusic = document.querySelectorAll('audio[id^="bg-music-"]');
        allMusic.forEach(audio => {
            audio.pause();
            audio.currentTime = 0;
        });
        
        // Включаем музыку для текущей комнаты
        const roomMusic = document.getElementById(`bg-music-${room}`);
        if (roomMusic) {
            roomMusic.volume = 0.3;
            roomMusic.play().catch(e => {
                console.log('Автовоспроизведение музыки заблокировано:', e);
            });
        }
    }
    
    // Воспроизводим музыку текущей комнаты при загрузке
    const currentRoom = document.querySelector('.room')?.classList[1]; // Получаем комнату из класса
    if (currentRoom) {
        changeRoomMusic(currentRoom);
    }

    // Обработка решения головоломок
    const puzzleForms = document.querySelectorAll('.puzzle-form');
    console.log('Puzzle forms found:', puzzleForms.length);
    
    puzzleForms.forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const answer = formData.get('answer');
            const puzzleId = this.dataset.puzzleId;
            const resultMessage = this.querySelector('.result-message');
            
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
                    this.remove();
                    checkVictory();
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
                        updateHearts(data.hearts);
                    }
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    });
    
    // Навигация по комнатам
    const roomButtons = document.querySelectorAll('.room-button');
    console.log('Room buttons found:', roomButtons.length);
    
    roomButtons.forEach(button => {
        button.addEventListener('click', async function(e) {
            e.preventDefault();
            const room = this.dataset.room;
            console.log('Changing room to:', room);
            
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
                    // Меняем музыку перед перезагрузкой
                    changeRoomMusic(room);
                    // Полная перезагрузка страницы
                    setTimeout(() => {
                        window.location.reload();
                    }, 300);
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
        const heartElements = document.querySelectorAll('.heart');
        heartElements.forEach((heart, index) => {
            if (index >= hearts) {
                heart.classList.add('broken');
            } else {
                heart.classList.remove('broken');
            }
        });
    }
    
    function checkVictory() {
        const solvedPuzzles = document.querySelectorAll('.puzzle-form');
        if (solvedPuzzles.length === 0) {
            // Проверяем, все ли загадки решены
            setTimeout(() => {
                window.location.href = '/victory/';
            }, 1000);
        }
    }
    
    // Инициализация отображения сердец
    const initialHearts = document.querySelectorAll('.heart').length;
    updateHearts(initialHearts);
});