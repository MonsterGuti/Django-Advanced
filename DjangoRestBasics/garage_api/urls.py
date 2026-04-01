from django.urls import path
from garage_api import views

urlpatterns = [
    path('manufacturers/', views.ListManufacturerApiView.as_view(), name='manufacturer-list'),
    path('cars/', views.ListCarApiView.as_view(), name='car-list'),
    path('cars/stats/', views.CarStatsApiView.as_view(), name='car-stats'),
    path('cars/<int:pk>/', views.CarDetailApiView.as_view(), name='car-detail'),
]