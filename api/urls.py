from django.urls import path, include
from . import views

urlpatterns = [
    path('items/', views.ItemView.as_view(), name='item_view'),
    path('items/<int:pk>/', views.ItemDetailView.as_view()),
    path('rest-auth/', include('rest_auth.urls')),

]