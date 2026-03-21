from django import forms
from .models import Game
from .models import Review
class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'description', 'image', 'release_date', 'status', 'personal_rating']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']