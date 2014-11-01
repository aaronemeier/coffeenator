from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt

from webinterface.lib.common import page
from webinterface.lib.forms import UserCreationForm, ProfileCreationForm, \
    SettingsChangeForm
from webinterface.lib.models import UserProfile, Settings


def main(request):
    settings = page("settings", request)
    if not request.user.is_authenticated():
        return redirect('/login/')
    else:
        NewUserCreationForm = UserCreationForm()
        NewProfileCreationForm = ProfileCreationForm()
        Users = User.objects.values('id', 'username', 'first_name', 'last_name')
        UserProfiles = UserProfile.objects.values('language', 'is_admin')
        UserListForm = ""
        for i in xrange(0,len(Users)):
            UserListForm += "<tr>"
            UserListForm += "<td><input type=\"button\" class=\"deleteuser\" value=\""+ str(Users[i]['id']) + "\" /></td>"
            UserListForm += "<td>" + Users[i]['username'] + "</td>"
            UserListForm += "<td>" + Users[i]['first_name'] + "</td>"
            UserListForm += "<td>" + Users[i]['last_name'] + "</td>"
            if UserProfiles[i]['is_admin']:
                UserListForm += "<td>" + _("Administrator") + "</td>"
            else:
                UserListForm += "<td>" + _("User") + "</td>"
            UserListForm += "</tr>"
        ActualSettings = Settings.objects.get(id=1)
        NewSettingsChangeForm = SettingsChangeForm(instance=ActualSettings)
        return render(request, 'settings.html', {                  
            'page': settings,
            'UserListForm': UserListForm,
            'UserCreationForm': NewUserCreationForm,
            'ProfileCreationForm': NewProfileCreationForm,
            'SettingsChangeForm': NewSettingsChangeForm
        })

@csrf_exempt
def ajax(request):
    settings = page("settings", request)
    if not request.user.is_authenticated():
        return redirect('/login/')
    else:
        if request.method == 'POST' and settings.profile['is_admin']:
            if request.POST.get("deleteuser") is not None:
                # Delete user, profile
                DeleteUser = User.objects.get(id=request.POST.get("deleteuser"))
                DeleteProfile = UserProfile.objects.get(user=DeleteUser)
                DeleteProfile.delete()
                DeleteUser.delete()
                return redirect('/settings/')
            elif request.POST.get("createuser") is not None:
                # Check form
                NewUserForm = UserCreationForm(request.POST)
                NewProfileForm = ProfileCreationForm(request.POST)
                if NewUserForm.is_valid():
                    # Create user, profile
                    NewUser = NewUserForm.save()
                    NewUser.set_password(request.POST['password'])
                    NewUser.save()
                    NewProfile = NewProfileForm.save(commit=False)
                    NewProfile.user = NewUser
                    NewProfile.save()
                    messages = { 'info': _("User was created!")}
                else:
                    messages = { 'errors': NewUserForm.errors}
                return render(request, 'ajax.html', {
                    'messages': messages
                })
            elif request.POST.get("changesettings") is not None:
                NewSettingsForm = SettingsChangeForm(request.POST)
                if NewSettingsForm.is_valid():
                    # Save new settings
                    NewSettings = NewSettingsForm.save(commit=False)
                    NewSettings.id = 1
                    NewSettings.save()
                    messages = { 'info': _('Settings saved!')}
                    if request.POST.get('descale'):
                        # Descale coffeemachine
                        messages = { 'info': _('Coffeemachine will be descaled!')}
                else:
                    messages = { 'errors': NewSettings.errors}
                return render(request, 'ajax.html', {
                    'messages': messages
                })
        elif settings.profile['is_admin']:
            messages = { 'errors': _("You don't have permission to do this!") }
            return render(request, 'ajax.html', {'messages': messages })
        else:
            messages = { 'errors': _("wrong request") }
            return render(request, 'ajax.html', {'messages': messages })