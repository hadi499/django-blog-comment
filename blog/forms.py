from django import forms
from .models import BlogPost, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ('title', 'content',  'author', 'image')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
