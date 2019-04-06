from django.urls import path, include
from . import views

urlpatterns = [
    path('items/', views.ItemView.as_view(), name='item_view'),
    path('rest-auth/', include('rest_auth.urls')),

]