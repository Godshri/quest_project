from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Player, Puzzle
import json
import random
from django.utils import timezone

ROOM_NAMES = {
    'server': 'Серверная',
    'library': 'Библиотека', 
    'arcade': 'Аркадный автомат',
    'roof': 'Крыша',
    'start': 'Стартовая комната'
}

# Добавляем количество загадок для каждой комнаты
ROOM_PUZZLE_COUNTS = {
    'server': 3,
    'library': 3,
    'arcade': 3,
    'roof': 3
}

def index(request):
    return render(request, 'quest_app/index.html')

def game(request):
    # Получаем или создаем игрока
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
    
    
    if not player.check_activity():
        # Игрок неактивен - сбрасываем игру
        player.hearts = 5
        player.solved_puzzles = []
        player.assigned_puzzles = {}
        player.current_room = 'start'
        player.completed = False
        player.is_active = True
    
    # Обновляем время последней активности
    player.last_activity = timezone.now()
    player.save()
    
    # Инициализируем assigned_puzzles если их нет
    if not player.assigned_puzzles:
        player.assigned_puzzles = {}
        player.save()
    
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        
        if action == 'solve_puzzle':
            if player.hearts <= 0:
                return JsonResponse({'success': False, 'hearts': 0, 'game_over': True})

            puzzle_id = data.get('puzzle_id')
            answer = data.get('answer')

            # Проверяем, не решена ли уже эта загадка (более надежная проверка)
            if str(puzzle_id) in player.solved_puzzles:
                return JsonResponse({'success': True, 'already_solved': True})

            try:
                puzzle = Puzzle.objects.get(id=puzzle_id)

                if answer.lower() == puzzle.solution.lower():
                    # Добавляем загадку в решенные, если ее там еще нет
                    if str(puzzle_id) not in player.solved_puzzles:
                        player.solved_puzzles.append(str(puzzle_id))
                        player.save()
                    return JsonResponse({
                        'success': True,
                        'solved_count': len(player.solved_puzzles)  # Добавьте эту строку
                    })
                else:
                    # Сохраняем текущее количество сердец перед вычитанием
                    current_hearts = player.hearts
                    player.use_heart()
                    # Возвращаем обновленное количество сердец
                    return JsonResponse({
                        'success': False, 
                        'hearts': player.hearts,
                        'game_over': player.hearts <= 0
                    })
            except Puzzle.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Puzzle not found'})
        elif action == 'change_room':
            room = data.get('room')
            # Проверяем доступ к крыше
            if room == 'roof':
                # Проверяем, что решено 9 загадок (3 комнаты по 3 загадки)
                if len(player.solved_puzzles) < 9:
                    return JsonResponse({'success': False, 'message': 'Сначала решите все загадки в других комнатах!'})

            player.current_room = room
            player.save()

            # Возвращаем данные о новой комнате
            puzzles_data = []
            if room != 'start':
                # Если для этой комнаты еще не назначены загадки, назначаем их
                if room not in player.assigned_puzzles:
                    room_puzzles = list(Puzzle.objects.filter(room=room))
                    selected_puzzles = random.sample(room_puzzles, min(3, len(room_puzzles)))
                    player.assigned_puzzles[room] = [str(p.id) for p in selected_puzzles]
                    player.save()

                # Получаем загадки для комнаты
                assigned_ids = player.assigned_puzzles.get(room, [])
                puzzles = Puzzle.objects.filter(id__in=assigned_ids)
                puzzles_data = [{
                    'id': p.id,
                    'name': p.name,
                    'description': p.description,
                    'difficulty': p.difficulty,
                    'solved': str(p.id) in player.solved_puzzles
                } for p in puzzles]

            return JsonResponse({
                'success': True,
                'room': room,
                'room_name': ROOM_NAMES.get(room, room),
                'puzzles': puzzles_data,
                'solved_count': len(player.solved_puzzles),
                'hearts': player.hearts
            })
        
        elif action == 'reset_game':
            player.hearts = 5
            player.solved_puzzles = []
            player.assigned_puzzles = {}  # Очищаем назначенные загадки
            player.current_room = 'start'
            player.completed = False
            player.save()
            return JsonResponse({
                'success': True,
                'solved_count': len(player.solved_puzzles) 
            })
    
    # Получаем загадки для текущей комнаты
    puzzles = []
    if player.current_room != 'start':
        # Если для этой комнаты еще не назначены загадки, назначаем их случайным образом
        if player.current_room not in player.assigned_puzzles:
            room_puzzles = list(Puzzle.objects.filter(room=player.current_room))
            # Выбираем 3 случайные загадки для комнаты
            selected_puzzles = random.sample(room_puzzles, min(3, len(room_puzzles)))
            player.assigned_puzzles[player.current_room] = [str(p.id) for p in selected_puzzles]
            player.save()
        
        # Получаем назначенные загадки для комнаты
        assigned_ids = player.assigned_puzzles.get(player.current_room, [])
        puzzles = Puzzle.objects.filter(id__in=assigned_ids)
    
    # Считаем общее количество загадок (12)
    total_puzzles = 12
    
    context = {
        'player': player,
        'puzzles': puzzles,
        'room': player.current_room,
        'room_name': ROOM_NAMES.get(player.current_room, player.current_room),
        'total_hearts': 5,
        'total_puzzles': total_puzzles,
        'progress_percent': (len(player.solved_puzzles) / total_puzzles * 100) if total_puzzles > 0 else 0
    }
    return render(request, 'quest_app/room.html', context)

def victory(request):
    player_id = request.session.get('player_id')
    if player_id:
        try:
            player = Player.objects.get(id=player_id)
            # Проверяем, что решены все 12 загадок
            if len(player.solved_puzzles) >= 12:
                player.completed = True
                
                # Генерируем или получаем существующий код победы
                if not player.victory_code:
                    from .id_generator import generate_kvant_id
                    player.victory_code = generate_kvant_id()
                    player.save()
                
                return render(request, 'quest_app/victory.html', {
                    'player': player,
                    'unique_id': player.victory_code
                })
        except Player.DoesNotExist:
            pass
    return redirect('game')

def game_over(request):
    player_id = request.session.get('player_id')
    player = None
    if player_id:
        try:
            player = Player.objects.get(id=player_id)
        except Player.DoesNotExist:
            pass
    
    context = {'player': player} if player else {}
    return render(request, 'quest_app/game_over.html', context)