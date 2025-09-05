from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    path('game/', views.game, name='game'),
    path('victory/', views.victory, name='victory'),
    path('game-over/', views.game_over, name='game_over'),
]