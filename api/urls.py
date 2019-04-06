from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'', views.ItemView.as_view(), name='item_view'),
    url('rest-auth/', include('rest_auth.urls')),

]
