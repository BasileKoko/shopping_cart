from django.urls import path, include
from . import views

urlpatterns = [
    path('items/', views.ItemView.as_view()),
    path('items/<int:pk>/', views.ItemDetailView.as_view()),
    path('basket/add', views.BasketAddView.as_view()),
    path('basket/change/<int:pk>/', views.BasketChangeView.as_view()),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
]
