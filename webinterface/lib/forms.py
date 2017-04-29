'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
    Aaron Meier <aaron@bluespeed.org>
'''

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

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