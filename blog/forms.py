from django import forms
from .models import BlogComment

class BlogSearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search', 'required': 'required'})
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['commenter_name', 'comment']

        widgets = {
            'commenter_name' : forms.TextInput(attrs={'class': 'form-control me-auto text-black', 'placeholder': 'Enter Your Name', 'required': 'required'}),
            'comment' : forms.Textarea(attrs={'class': 'form-control text-black', 'rows': 5,'placeholder': 'Join the discussion and leave a comment!', 'required': 'required'})

        }
        slug = forms.CharField(
        widget=forms.HiddenInput()
    )
    def clean_comment(self):
        comment = self.cleaned_data['comment']
        if not comment:
            raise forms.ValidationError("Please enter a comment.")
        return comment
    
    def clean_commenter_name(self):
        commenter_name = self.cleaned_data['commenter_name']
        if not commenter_name:
            raise forms.ValidationError("Please enter your name.")
        return commenter_name