from django.contrib.auth.forms import forms, UserCreationForm
from django.contrib.auth.models import User
from .models import Rating

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['stars']