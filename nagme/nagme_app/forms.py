from django import forms
from django.contrib.auth.models import User
from nagme_app.models import Category, UserProfile
from phonenumber_field.modelfields import PhoneNumberField


class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True, label="Name")
    contact_number = PhoneNumberField()
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
        fields = ('phone_number','picture')