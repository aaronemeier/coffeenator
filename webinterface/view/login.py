from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt

from webinterface.lib.common import page
from webinterface.lib.forms import LoginForm


def main(request):
    login = page("login", request)
    NewLoginForm = LoginForm()
    return render(request, 'login.html', {
        'LoginForm': NewLoginForm,
        'page': login
    })

@csrf_exempt
def ajax(request):
    if request.method == 'POST':
        if request.POST.get("login") is not None:
            # Log in requested user
            AuthUser = authenticate(username=request.POST['username'], 
                                    password=request.POST['password'])
            if AuthUser is not None:
                if AuthUser.is_active:
                    login(request, AuthUser)
                    return HttpResponse('<script>window.location = "/dashboard/"</script>')
                else:
                    messages = { 'errors': _("User is locked.")}
                    return render(request, 'ajax.html', {'errors': messages })
            else:
                messages = { 'errors': _("Either username or password is wrong.")}
                return render(request, 'ajax.html', {'messages': messages })
        elif request.POST.get("logout") is not None:
            logout(request)
            return HttpResponse('<script>window.location = "/login/"</script>')