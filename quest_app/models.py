from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_room = models.CharField(max_length=50, default='start')
    collected_items = models.JSONField(default=list)
    solved_puzzles = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

class Puzzle(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    solution = models.CharField(max_length=200)
    room = models.CharField(max_length=50)
    order = models.IntegerField()

    def __str__(self):
        return self.name