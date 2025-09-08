from django.db import models
import random
from django.utils import timezone
from datetime import timedelta

class Player(models.Model):
    current_room = models.CharField(max_length=50, default='start')
    hearts = models.IntegerField(default=5)
    solved_puzzles = models.JSONField(default=list)
    assigned_puzzles = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    victory_code = models.CharField(max_length=50, blank=True, null=True) 
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def check_activity(self):
        """Проверяет, активен ли игрок (в пределах 5 минут)"""
        return timezone.now() - self.last_activity < timedelta(minutes=5)
    
    def use_heart(self):
        self.hearts -= 1
        self.save()
        return self.hearts > 0

    def __str__(self):
        return f"Player {self.id} - {self.current_room}"

class Puzzle(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    solution = models.CharField(max_length=200)
    room = models.CharField(max_length=50)
    difficulty = models.IntegerField(default=1)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.room} - {self.name}"

    class Meta:
        ordering = ['room', 'order']