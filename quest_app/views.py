from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Player, Puzzle
import json

# Словарь для перевода названий комнат
ROOM_NAMES = {
    'server': 'Серверная',
    'library': 'Библиотека', 
    'arcade': 'Аркадный автомат',
    'roof': 'Крыша',
    'start': 'Стартовая комната'
}

def index(request):
    return render(request, 'quest_app/index.html')

@login_required
def game(request):
    player, created = Player.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        
        if action == 'solve_puzzle':
            puzzle_id = data.get('puzzle_id')
            answer = data.get('answer')
            puzzle = Puzzle.objects.get(id=puzzle_id)
            
            if answer.lower() == puzzle.solution.lower():
                if puzzle_id not in player.solved_puzzles:
                    player.solved_puzzles.append(puzzle_id)
                    player.save()
                return JsonResponse({'success': True})
            return JsonResponse({'success': False})
        
        elif action == 'change_room':
            room = data.get('room')
            player.current_room = room
            player.save()
            return JsonResponse({'success': True})
    
    puzzles = Puzzle.objects.filter(room=player.current_room).order_by('order')
    context = {
        'player': player,
        'puzzles': puzzles,
        'room': player.current_room,
        'room_name': ROOM_NAMES.get(player.current_room, player.current_room)  # Добавляем русское название
    }
    return render(request, 'quest_app/room.html', context)

@login_required
def victory(request):
    player = Player.objects.get(user=request.user)
    if len(player.solved_puzzles) >= 4:  # Все головоломки решены
        return render(request, 'quest_app/victory.html')
    return redirect('game')