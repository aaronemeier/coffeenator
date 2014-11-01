from datetime import datetime
from os import system

from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt

from webinterface.lib.common import page
from webinterface.lib.forms import CoffeeOrderForm
from webinterface.lib.models import Coffee


def main(request):
    orders = page("orders", request)
    if not request.user.is_authenticated():
        return redirect('/login/')
    else:
        NewCoffeeOrderForm = CoffeeOrderForm()
        CoffeeList = Coffee.objects.filter(datetime__gte=datetime.now())
        CoffeeListForm = ""
        for i in xrange(0,len(CoffeeList)):
            CoffeeListForm += "<tr>"
            CoffeeListForm += "<td>"+ str(CoffeeList[i].datetime) + "</td>"
            CoffeeListForm += "<td>"+ str(CoffeeList[i].user) + "</td>"
            CoffeeListForm += "<td>" + CoffeeList[i].typ + "</td>"
            CoffeeListForm += "<td>" + CoffeeList[i].cups + "</td>"
            CoffeeListForm += "</tr>"
        return render(request, 'orders.html', {
           'page': orders,
           'CoffeeOrderForm': NewCoffeeOrderForm,
           'CoffeeListForm': CoffeeListForm
        })

@csrf_exempt
def ajax(request):
    orders = page("orders", request)
    if not request.user.is_authenticated():
        return redirect('/login/')
    else:
        if request.method == 'POST':
            if request.POST.get('ordercoffee') is not None:
                # Check form
                NewCoffeeOrderForm = CoffeeOrderForm(request.POST)
                if NewCoffeeOrderForm.is_valid():
                    if request.POST.get('now') is not None:
                        # Make coffee now
                        NewCoffee = NewCoffeeOrderForm.save(commit=False)
                        NewCoffee.user = request.user
                        NewCoffee.datetime = datetime.now()
                        NewCoffee.save()
                        # Make cronjob
                        system('python /usr/share/coffeenator/webinterface/lib/coffeemachine.py -t ' + NewCoffee.typ + ' -n ' + NewCoffee.cups)
                        messages = {'info': _("Your coffee will be avaiable shortly.")}
                    elif not request.POST.get('datetime') == "":
                        # Schedule coffee for future
                        NewCoffee = NewCoffeeOrderForm.save(commit=False)
                        NewCoffee.user = request.user
                        NewCoffee.save()
                        messages = {'info': _("Your coffee order was placed for ") + unicode(NewCoffee.datetime)}
                    else:
                        messages = {'errors': _("Select either an exact time or now.")}
                else:
                    messages = {'errors': NewCoffeeOrderForm.errors}
                return render(request, 'ajax.html', {'messages': messages })
            elif request.POST.get('stoporders') is not None:
                if orders.profile['is_admin']:
                    messages = {'info': _("Coffee queue cleared!")}
                else:
                    messages = {'errors': _("You don't have permission to do this!")}
                return render(request, 'ajax.html', {'messages': messages })
            else:
                messages = { 'errors': _("wrong request") }
                return render(request, 'ajax.html', {'messages': messages })
