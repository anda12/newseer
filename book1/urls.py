from django.conf.urls import include, url
from django.urls import path
from book1.views import jddsj,page

urlpatterns = [
    url(r'^$',jddsj.home),  
    url(r'^home/$',jddsj.home,name="home"),
    url(r'^(?P<slug>[\w./-]+)/$', page, name='page'),
    url(r'^$', page, name='homepage'),

]