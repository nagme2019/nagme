from django import forms
from django.contrib.auth.models import User
from nagme_app.models import Category, UserProfile, Nag


class ContactForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    message = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(),
    )
    source = forms.CharField(  # A hidden input for internal use
        max_length=50,  # tell from which page the user sent the message
        widget=forms.HiddenInput()
    )

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        message = cleaned_data.get('message')
        if not name and not email and not message:
            raise forms.ValidationError('You have to write something!')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone_number', 'picture')


class NagForm(forms.ModelForm):
    class Meta:
        model = Nag
        fields = ('category', 'author', 'text')