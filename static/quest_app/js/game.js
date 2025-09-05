document.addEventListener('DOMContentLoaded', function() {
    // Воспроизведение музыки
    const bgMusic = document.getElementById('bg-music');
    const successSound = document.getElementById('success-sound');
    const failSound = document.getElementById('fail-sound');
    
    // Попытка воспроизвести музыку при взаимодействии пользователя
    document.addEventListener('click', function() {
        if (bgMusic.paused) {
            bgMusic.volume = 0.3;
            bgMusic.play().catch(() => {});
        }
    }, { once: true });

    // Обработка решения головоломок
    const puzzleForms = document.querySelectorAll('.puzzle-form');
    puzzleForms.forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const answer = formData.get('answer');
            const puzzleId = this.dataset.puzzleId;
            const resultMessage = this.querySelector('.result-message');
            
            try {
                const response = await fetch('/game/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        action: 'solve_puzzle',
                        puzzle_id: puzzleId,
                        answer: answer
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    successSound.play();
                    resultMessage.textContent = '✅ Правильно! Загадка решена!';
                    resultMessage.className = 'result-message success';
                    this.remove();
                    checkVictory();
                } else {
                    failSound.play();
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
    const roofButton = document.getElementById('roof-button');
    
    roomButtons.forEach(button => {
        button.addEventListener('click', async function() {
            const room = this.dataset.room;
            
            try {
                const response = await fetch('/game/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        action: 'change_room',
                        room: room
                    })
                });
                
                const data = await response.json();
                if (data.success) {
                    location.reload();
                } else if (data.message) {
                    alert(data.message);
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    });
    
    function updateHearts(hearts) {
        const heartElements = document.querySelectorAll('.heart');
        heartElements.forEach((heart, index) => {
            if (index >= hearts) {
                heart.classList.add('broken');
            }
        });
    }
    
    function checkVictory() {
        const solvedPuzzles = document.querySelectorAll('.puzzle-form');
        if (solvedPuzzles.length === 0) {
            // Проверяем, все ли загадки решены
            fetch('/victory/')
                .then(response => {
                    if (response.ok) {
                        window.location.href = '/victory/';
                    }
                });
        }
    }
    
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
});