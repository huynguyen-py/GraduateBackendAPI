"""API_Server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static
from django.conf import settings

admin.site.site_header = "MediCom - Admin Portal"
admin.site.site_title = "MediCom - Admin Portal"


schema_view = get_schema_view(
   openapi.Info(
      title="Graduate API",
      default_version='v1',
      description="My description",
      terms_of_service="https://www.medicom-live.com/policies/terms/",
      contact=openapi.Contact(email="contact@medicom.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('acp/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/users/', include('API_Source.urls')),
    path('api/articles/', include('API_Article.urls')),
    path('api/diagnosis/', include('API_Diagnosis.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)