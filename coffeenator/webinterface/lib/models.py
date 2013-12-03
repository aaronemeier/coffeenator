from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

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