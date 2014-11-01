from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'webinterface.view.dashboard.main'),
    url(r'^dashboard/$', 'webinterface.view.dashboard.main'),
    url(r'^login/$', 'webinterface.view.login.main'),
    url(r'^login/ajax/$', 'webinterface.view.login.ajax'),
    url(r'^settings/$', 'webinterface.view.settings.main'),
    url(r'^settings/ajax/$', 'webinterface.view.settings.ajax'),
    url(r'^orders/$', 'webinterface.view.orders.main'),
    url(r'^orders/ajax/$', 'webinterface.view.orders.ajax'),
)