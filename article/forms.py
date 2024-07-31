from django.forms import ModelForm
from .models import *
from django import forms
from django_summernote.widgets import SummernoteWidget


class ArticleCreateForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'slug', 'content', 'image', 'status', 'tags']
        labels = {
            'tags': 'Category'
        }
        widgets ={
            'tags': forms.CheckboxSelectMultiple(attrs={"class": 'display:flex; flex-wrap:wrap;'}),
            'content': SummernoteWidget()
        }

class CommentCreateForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'rows':2, 'placeholder':'Add Comment ...'})
        }
        labels = {
            'body': ""
        }


class EmailArticleForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)