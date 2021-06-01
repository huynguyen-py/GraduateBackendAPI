from django.urls import path, include
# from rest_framework.routers import DefaultRouter
from rest_framework.routers import DefaultRouter

from .views import ListCreateDiagnosisView, DiagnosisDetailView, predictView


urlpatterns = [
    path('', ListCreateDiagnosisView.as_view(), name="list-diagnosis"),
    path('<int:pk>/', DiagnosisDetailView.as_view(), name="detail-diagnosis"),
    path('predict/', predictView.as_view(), name="predict-diagnosis"),
]