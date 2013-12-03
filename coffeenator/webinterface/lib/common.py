from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect
from django.utils import translation

from webinterface.lib.models import UserProfile, Settings

class page():
    """ Page settings """
    index = (("dashboard", _("DASHBOARD")),
             ("settings", _("SETTINGS")),
             ("orders", _("ORDERS")))
    navigation, title, profile = "", "", ""
    settings = Settings.objects.get(id=1)
    def __init__(self, name, request):
        for i in xrange(0,len(self.index)):
            if self.index[i][0] == name:
                self.title = self.index[i][1]
                self.navigation += "<li class=\"active\"><a href=\"/"+ self.index[i][0] +"\">" + self.index[i][1] + "</a></li>"
            else:
                self.navigation += "<li><a href=\"/"+ self.index[i][0] +"\">" + self.index[i][1] + "</a></li>"
        if request.user.is_authenticated():
            Properties = UserProfile.objects.get(user=request.user.id)
            self.profile = {'username': request.user,
                           'language': Properties.language,
                           'is_admin': Properties.is_admin}