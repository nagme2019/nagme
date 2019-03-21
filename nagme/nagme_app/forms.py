from django import forms
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from nagme_app.models import Category, UserProfile, Nag


class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True, label="Name")
    contact_email=forms.EmailField(max_length=500, label="Email")
    content = forms.CharField(
        required=True,
        widget=forms.Textarea,
        label="Message"
    )


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
