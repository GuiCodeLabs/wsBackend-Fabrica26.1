import os
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Game
from .forms import GameForm

API_KEY = os.getenv('RAWG_API_KEY')

@login_required
def game_list(request):
    games = Game.objects.filter(user=request.user)
    return render(request, 'games/game_list.html', {'games': games})

@login_required
def game_detail(request, id):
    game = get_object_or_404(Game, id=id, user=request.user)
    return render(request, 'games/game_detail.html', {'game': game})

@login_required
def create_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.user = request.user
            game.save()
            return redirect('games:game_list')
    else:
        form = GameForm()

    return render(request, 'games/create_game.html', {'form': form})

@login_required
def update_game(request, id):
    game = get_object_or_404(Game, id=id, user=request.user)

    if request.method == 'POST':
        form =GameForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            return redirect('games:game_list') 
            
    else:
        form = GameForm(instance=game)
    
    return render(request, 'games/update_game.html', {'form': form})

@login_required
def delete_game(request, id):
    game = get_object_or_404(Game, id=id, user=request.user)

    if request.method == 'POST':
        game.delete()
        return redirect('games:game_list')

    return render(request, 'games/delete_game.html', {'game': game})

@login_required
def search_games(request):
    query = request.GET.get('q')
    games = []

    if query:
        url = f"https://api.rawg.io/api/games?search={query}&key={API_KEY}"
        response = requests.get(url)
        data = response.json()
        games = data.get('results', [])

    return render(request, 'games/search_games.html', {'games': games})

@login_required
def save_api_game(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.POST.get('image')
        release_date = request.POST.get('release_date')
        api_id = request.POST.get('api_id')

        game_exists = Game.objects.filter(user=request.user, api_id=api_id).exists()

        if not game_exists:
            Game.objects.create(
                user=request.user,
                title=title,
                description=description or '',
                image=image or '',
                release_date=release_date if release_date else None,
                api_id=api_id if api_id else None,
            )

        return redirect('games:game_list')