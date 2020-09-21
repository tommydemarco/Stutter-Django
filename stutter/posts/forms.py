from django import forms
from .models import Post

class PostCreationForm(forms.ModelForm):
    '''model form for post creation'''

    class Meta:
        model = Post
        fields = ['content']
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > 300:
            raise forms.ValidationError('This post is too long')
        else:
            return content 
    
