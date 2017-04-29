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

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    is_admin = models.BooleanField(default=False)
    language_choices = ('de', 'en')
    language_choices = (('de', _('German')), ('en', _('English')))
    language = models.CharField(max_length=2, default="de", choices=language_choices)

class Settings(models.Model):
    force_ssl = models.BooleanField(default=False)
    welcome_message = models.CharField(max_length=250)
    telnet = models.BooleanField(default=False)
    
class Coffee(models.Model):
    user = models.ForeignKey(User)
    typ_choices = (('small', _('Small Coffee')),
                    ('medium', _('Medium Coffee')),
                    ('long', _('Long Coffee')))
    cups_choices = (('1', _('One cup')),
                    ('2', _('Two cups')))
    typ = models.CharField(max_length=10, choices=typ_choices, default='small')
    cups = models.CharField(max_length=10, choices=cups_choices, default=1)
    datetime = models.DateTimeField()