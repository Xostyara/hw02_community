from django import forms
from django import forms  # Импортируем модуль forms, из него возьмём класс ModelForm
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("text", "group")
    
