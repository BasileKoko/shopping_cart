from django.urls import path, include
from . import views

urlpatterns = [
    path('items/', views.ItemView.as_view()),
    path('items/<int:pk>/', views.ItemDetailView.as_view()),
    path('basket/', views.BasketView.as_view()),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
]
