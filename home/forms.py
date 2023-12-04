from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control  width-100%',
            'id': 'name',
            'placeholder': 'Enter your name',
        }),
        label='Full Name'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control  width-100%',
            'id': 'email',
            'placeholder': 'name@example.com',
        }),
        label='Email Address'
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control  width-100%',
            'id': 'phone',
            'placeholder': '+(123) 456-7890',
        }),
        label='Phone'
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control  width-100%',
            'id': 'message',
            'placeholder': 'Enter your message here',
            'style': 'height: 8rem',
        }),
        label='Message'
    )