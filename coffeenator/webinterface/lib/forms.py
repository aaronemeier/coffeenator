from django import forms
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from webinterface.lib.models import UserProfile, Settings, Coffee

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ["username", "password",  "first_name", "last_name", "email"]

class ProfileCreationForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["language", "is_admin"]

class SettingsChangeForm(forms.ModelForm):
    descale = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    welcome_message = forms.CharField(widget=forms.Textarea(attrs={'rows':5, 'cols':30}))
    class Meta:
        model = Settings
        fields = ["force_ssl", "welcome_message", "telnet"]

class LoginForm(forms.ModelForm):
    remember = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    password = forms.CharField(widget=forms.PasswordInput())  
    class Meta:
        model = User
        fields = ["username", "password"]
        
class CoffeeOrderForm(forms.ModelForm):
    typ = forms.ChoiceField(widget=forms.RadioSelect, required=True, choices=Coffee.typ_choices)
    cups = forms.ChoiceField(widget=forms.RadioSelect, required=True, choices=Coffee.cups_choices)
    datetime = forms.DateTimeField(required=False)
    now = forms.BooleanField(required=False)
    class Meta:
        model = Coffee
        fields = ["typ", "cups", "datetime"]