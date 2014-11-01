from collections import Counter
from datetime import datetime, timedelta
import math

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext as _

import uptime
from webinterface.lib.common import page
from webinterface.lib.models import Coffee


def main(request):
    dashboard = page("dashboard", request)
    if not request.user.is_authenticated():
        return redirect('/login/')
    else:
        # Create top user list
        TopUsers = {0: {'username': '','coffees': 0}}
        week_start = datetime.now() - timedelta(5)
        Users = User.objects.values('id', 'username', 'first_name', 'last_name')
        i=0
        for user in Users:
            TopUsers.update({i: {'username': user['username'],
                                 'coffees': len(Coffee.objects.filter(datetime__range=[week_start, datetime.now()], user__username=user['username'])) }})
            i+=1
        Temp = {}
        for i in xrange(0,len(TopUsers)):
            for j in xrange(i+1, len(TopUsers)):
                if TopUsers[i]['coffees'] < TopUsers[j]['coffees']:
                    Temp = TopUsers[i]
                    TopUsers[i] = TopUsers[j]
                    TopUsers[j] = Temp
        TopUsersList = ""
        for i in TopUsers:
            if i<5:
                TopUsersList += "<tr>"
                TopUsersList += "<td>" + TopUsers[i]['username'] + "</td>"
                TopUsersList += "<td>" + str(TopUsers[i]['coffees']) + "</td>"
                TopUsersList += "</tr>"
        # Create coffee consum chart
        ConsumChart = { 1: {'month': _("January"), 'small': 0, 'middle': 0, 'long': 0},
                        2: {'month': _("February"), 'small': 0, 'middle': 0, 'long': 0},
                        3: {'month': _("March"), 'small': 0, 'middle': 0, 'long': 0},
                        4: {'month': _("April"), 'small': 0, 'middle': 0, 'long': 0},
                        5: {'month': _("May"), 'small': 0, 'middle': 0, 'long': 0},
                        6: {'month': _("June"), 'small': 0, 'middle': 0, 'long': 0},
                        7: {'month': _("July"), 'small': 0, 'middle': 0, 'long': 0},
                        8: {'month': _("August"), 'small': 0, 'middle': 0, 'long': 0},
                        9: {'month': _("September"), 'small': 0, 'middle': 0, 'long': 0},
                        10: {'month': _("October"), 'small': 0, 'middle': 0, 'long': 0},
                        11: {'month': _("November"), 'small': 0, 'middle': 0, 'long': 0},
                        12: {'month': _("December"), 'small': 0, 'middle': 0, 'long': 0}}
        for i in ConsumChart:
            start, end = "",""
            start = datetime(datetime.now().year, i, 01, 00, 00, 00)
            if i == 2:
                try:
                    end = datetime(datetime.now().year, i, 29, 23, 59, 59)
                except ValueError:
                    end = datetime(datetime.now().year, i, 28, 23, 59, 59)
            else:
                try:
                    end = datetime(datetime.now().year, i, 31, 23, 59, 59)
                except ValueError:
                    end = datetime(datetime.now().year, i, 30, 23, 59, 59)
            for value in ConsumChart[i]:
                if not value == 'month':
                    ConsumChart[i][value] = len(Coffee.objects.filter(datetime__range=[start, end], typ__exact=value))
        ConsumChartList = "['" + _("Month") + "','" + _("Small coffees") + "','" + _("Middle coffees")  + "','" + _("Long coffees") + "'],"
        for i in ConsumChart:
            ConsumChartList +=  "['" + ConsumChart[i]['month'] + "', "
            ConsumChartList += str(ConsumChart[i]['small']) + ","
            ConsumChartList += str(ConsumChart[i]['middle']) + ","
            ConsumChartList += str(ConsumChart[i]['long']) + "],"
        return render(request, 'dashboard.html', {               
            'page': dashboard,
            'TopUsersList': TopUsersList,
            'uptime': uptime.boottime(),
            'ConsumChartList': ConsumChartList
        })