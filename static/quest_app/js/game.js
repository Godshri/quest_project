document.addEventListener('DOMContentLoaded', function() {
    // Обработка решения головоломок
    const puzzleForms = document.querySelectorAll('.puzzle-form');
    puzzleForms.forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const answer = formData.get('answer');
            const puzzleId = this.dataset.puzzleId;
            
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
                    alert('Поздравляем! Головоломка решена! 🎉');
                    this.remove();
                    // Проверяем победу
                    checkVictory();
                } else {
                    alert('Неверный ответ. Попробуйте еще раз!');
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    });
    
    // Навигация по комнатам
    const roomButtons = document.querySelectorAll('.room-button');
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
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    });
    
    function checkVictory() {
        // Можно добавить проверку количества решенных головоломок
        const solvedPuzzles = document.querySelectorAll('.puzzle-form');
        if (solvedPuzzles.length === 0) {
            setTimeout(() => {
                window.location.href = '/victory/';
            }, 2000);
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