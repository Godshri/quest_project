from django.contrib import admin
from .models import Player, Puzzle

@admin.register(Puzzle)
class PuzzleAdmin(admin.ModelAdmin):
    list_display = ['name', 'room', 'order']
    list_filter = ['room']

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['id', 'current_room', 'hearts', 'created_at']
    readonly_fields = ['created_at']