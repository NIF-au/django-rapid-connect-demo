from django.conf.urls import patterns, url

from rc import views

urlpatterns = patterns('',
                    url(r'^$',          views.root,     name='root'),
                    url(r'^welcome$',   views.welcome,  name='welcome'),
                    url(r'^logout$',    views.logout,   name='logout'),
                    url(r'^auth/jwt$',  views.auth,     name='auth'),
                    )

