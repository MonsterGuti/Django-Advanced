from django.urls import path, include
from rest_framework.routers import DefaultRouter

from garage_api.views import ListCreateCarApiView, CarStatsView, RetrieveUpdateDestroyCarApiView, \
    ListCreateManufacturerApiView, PartModelViewSet, AdminDasboardView

router = DefaultRouter()
router.register('parts', PartModelViewSet, basename='parts')

urlpatterns = [
    path('cars/', include([
        path('', ListCreateCarApiView.as_view(), name='car-list-create'),
        path('<int:pk>/', RetrieveUpdateDestroyCarApiView.as_view(), name='car-detail'),
        path('stats/', CarStatsView.as_view(), name='car-stats'),
    ])),
    path('manufacturers/', ListCreateManufacturerApiView.as_view(), name='manufacturer-list'),
    path('admin-dashboard/', AdminDasboardView.as_view(), name='admin-dashboard'),

] + router.urls
