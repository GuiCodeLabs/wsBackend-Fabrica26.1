from django.urls import path
from .views import game_list, game_detail, create_game, update_game

app_name = 'games'

urlpatterns = [
    path('', game_list, name='game_list'),
    path('game/<int:id>/', game_detail, name='game_detail'),
    path('create/', create_game, name='create_game'),
    path('update/<int:id>/', update_game, name='update_game'),
]