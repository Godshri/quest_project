from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Player, Puzzle  # Убедитесь, что Puzzle импортирована
import json
import random

ROOM_NAMES = {
    'server': 'Серверная',
    'library': 'Библиотека', 
    'arcade': 'Аркадный автомат',
    'roof': 'Крыша',
    'start': 'Стартовая комната'
}

def index(request):
    return render(request, 'quest_app/index.html')

def game(request):
    # Получаем или создаем игрока без привязки к пользователю
    player_id = request.session.get('player_id')
    if player_id:
        try:
            player = Player.objects.get(id=player_id)
        except Player.DoesNotExist:
            player = Player.objects.create()
            request.session['player_id'] = player.id
    else:
        player = Player.objects.create()
        request.session['player_id'] = player.id
    
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        
        if action == 'solve_puzzle':
            if player.hearts <= 0:
                return JsonResponse({'success': False, 'hearts': 0, 'game_over': True})
            
            puzzle_id = data.get('puzzle_id')
            answer = data.get('answer')
            puzzle = Puzzle.objects.get(id=puzzle_id)
            
            if answer.lower() == puzzle.solution.lower():
                if str(puzzle_id) not in player.solved_puzzles:
                    player.solved_puzzles.append(str(puzzle_id))
                    player.save()
                return JsonResponse({'success': True})
            else:
                player.use_heart()
                return JsonResponse({
                    'success': False, 
                    'hearts': player.hearts,
                    'game_over': player.hearts <= 0
                })
        
        elif action == 'change_room':
            room = data.get('room')
            # Проверяем доступ к крыше
            if room == 'roof':
                total_puzzles = Puzzle.objects.exclude(room='roof').count()
                if len(player.solved_puzzles) < total_puzzles:
                    return JsonResponse({'success': False, 'message': 'Сначала решите все загадки в других комнатах!'})
            player.current_room = room
            player.save()
            return JsonResponse({'success': True})
        
        elif action == 'reset_game':
            player.hearts = 5
            player.solved_puzzles = []
            player.current_room = 'start'
            player.completed = False
            player.save()
            return JsonResponse({'success': True})
    
    # Получаем случайные загадки для комнаты
    if player.current_room != 'start':
        puzzles = player.get_random_puzzles(player.current_room, 3)
    else:
        puzzles = []
    
    context = {
    'player': player,
    'puzzles': puzzles,
    'room': player.current_room,
    'room_name': ROOM_NAMES.get(player.current_room, player.current_room),
    'total_hearts': 5,
    'total_puzzles': Puzzle.objects.count(),
    'progress_percent': (len(player.solved_puzzles) / Puzzle.objects.count() * 100) if Puzzle.objects.count() > 0 else 0
    }
    return render(request, 'quest_app/room.html', context)

def victory(request):
    player_id = request.session.get('player_id')
    if player_id:
        try:
            player = Player.objects.get(id=player_id)
            if len(player.solved_puzzles) >= Puzzle.objects.count():
                player.completed = True
                player.save()
                return render(request, 'quest_app/victory.html', {'player': player})
        except Player.DoesNotExist:
            pass
    return redirect('game')

def game_over(request):
    return render(request, 'quest_app/game_over.html')

# УДАЛИТЕ эту функцию - она уже есть в методе класса Player
# def get_random_puzzles(self, room, count=3):
#     puzzles = list(Puzzle.objects.filter(room=room))
#     if len(puzzles) <= count:
#         return puzzles
#     return random.sample(puzzles, count)