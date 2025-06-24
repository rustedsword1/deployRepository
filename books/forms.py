from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    category = forms.ChoiceField(
        choices=Book.CATEGORY_CHOICES,  
        label='カテゴリ',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'category', 'comment', 'rating', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'rating': forms.Select(choices=[(i, str(i)) for i in range(1, 6)],
                                   attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
