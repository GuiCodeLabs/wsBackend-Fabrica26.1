from django.urls import path
from .views import game_list, game_detail, create_game, update_game, delete_game, search_games, save_api_game

app_name = 'games'

urlpatterns = [
    path('', game_list, name='game_list'),
    path('game/<int:id>/', game_detail, name='game_detail'),
    path('create/', create_game, name='create_game'),
    path('update/<int:id>/', update_game, name='update_game'),
    path('delete/<int:id>/', delete_game, name='delete_game'),
    path('search/', search_games, name='search_games'),
    path('save-api-game/', save_api_game, name='save_api_game'),
]