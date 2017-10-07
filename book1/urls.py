from django.conf.urls import include, url 
from book1.views import hello

urlpatterns = [
    url(r'^$',hello),  
]