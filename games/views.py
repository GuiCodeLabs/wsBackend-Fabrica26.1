from django.shortcuts import render, get_object_or_404
from .models import Game

def game_list(request):
    games = Game.objects.all()
    return render(request, 'games/game_list.html', {'games': games})

def game_detail(request, id):
    game = get_object_or_404(Game, id=id)
    return render(request, 'games/game_detail.html', {'game': game})