from django.urls import path, include
from . import views

urlpatterns = [
    path('items/', views.ItemView.as_view()),
    path('items/<int:pk>/', views.ItemDetailView.as_view()),
    path('basket/add', views.BasketAddListView.as_view()),
    path('basket/change/<int:pk>/', views.BasketChangeView.as_view()),
    path('basket/change/add_to_trolley/<int:pk>/', views.BasketAddItemToTrolleyView.as_view()),
    path('trolley/add', views.TrolleyAddListView.as_view()),
    path('trolley/change/<int:pk>/', views.TrolleyChangeView.as_view()),
    path('order/add/', views.OrderAddView.as_view()),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
]
