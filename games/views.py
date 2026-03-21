import os
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Game, Review
from .forms import GameForm, ReviewForm
from deep_translator import GoogleTranslator

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
        form = GameForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            return redirect('games:game_list')
    else:
        form = GameForm(instance=game)

    return render(request, 'games/update_game.html', {
        'form': form,
        'game': game
    })

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
        image = request.POST.get('image')
        release_date = request.POST.get('release_date')
        api_id = request.POST.get('api_id')
        status = request.POST.get('status', 'backlog') # Pega o status ou usa backlog como padrão

        game_exists = Game.objects.filter(user=request.user, api_id=api_id).exists()

        if not game_exists:
            # Busca a descrição completa na API usando o ID
            description = ''
            if api_id:
                try:
                    detail_url = f"https://api.rawg.io/api/games/{api_id}?key={API_KEY}"
                    detail_response = requests.get(detail_url)
                    if detail_response.status_code == 200:
                        detail_data = detail_response.json()
                        # description_raw vem sem tags HTML, o que é melhor para seu design
                        description_en = detail_data.get('description_raw', '') or detail_data.get('description', '')
                        
                        if description_en:
                            try:
                                description = GoogleTranslator(source='auto', target='pt').translate(description_en)
                            except Exception as e:
                                print(f"Erro na tradução: {e}")
                                description = description_en
                except Exception as e:
                    print(f"Erro ao buscar detalhes: {e}")

            Game.objects.create(
                user=request.user,
                title=title,
                description=description,
                image=image or '',
                release_date=release_date if release_date else None,
                api_id=api_id if api_id else None,
                status=status
            )

        return redirect('games:game_list')

@login_required
def add_review(request, id):
    game = get_object_or_404(Game, id=id, user=request.user)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.game = game
            review.user = request.user
            review.save()
            return redirect('games:game_detail', id=game.id)
    else:
        form = ReviewForm()

    return render(request, 'games/add_review.html', {'form': form, 'game': game})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('games:game_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})