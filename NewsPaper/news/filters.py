import django_filters as filters
from django_filters import FilterSet
from django import forms
from .models import Post, Author


class PostFilter(FilterSet):

    title = filters.CharFilter(
        label='Title', 
        lookup_expr='icontains',
        widget = forms.TextInput(attrs={
            'placeholder': 'Title', 
            'class':'form-control',        
        }))
    
    creationData = filters.CharFilter(
        label='Created later than', 
        lookup_expr='gt',
        widget = forms.TextInput(attrs={
            'placeholder': 'YYYY-MM-DD HH:MM', 
            'class':'form-control',
        }))
    
    author = filters.ModelChoiceFilter(
        label = 'Author',
        lookup_expr='exact',
        queryset = Author.objects.all(),
        widget = forms.Select(attrs={
            'class': 'form-select',
        }))
    

    class Meta:
        model = Post
        fields = ('author', 'title', 'creationData')


    # class Meta:
    #     model = Post
    #     fields = {
    #         'title'=: ['icontains'],
    #         'creationData': ['gt'],
    #         'categoryType': ['exact']
    #     }