from django.shortcuts import render, redirect, get_object_or_404
from .models import Game
from .forms import GameForm


def game_list(request):
    games = Game.objects.all()
    return render(request, 'games/game_list.html', {'games': games})

def game_detail(request, id):
    game = get_object_or_404(Game, id=id)
    return render(request, 'games/game_detail.html', {'game': game})

def create_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('games:game_list')
    else:
        form = GameForm()

    return render(request, 'games/create_game.html', {'form': form})

