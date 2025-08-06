"""
URL configuration for poll_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include, re_path
from polls.views import VoteAPIView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.shortcuts import redirect
# from django.contrib.auth import views as auth_views

schema_view = get_schema_view(
    openapi.Info(
        title="Online Poll System API",
        default_version='v1',
        description="API documentation for the Online Poll System",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="iankerich254@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('polls.urls')),
    re_path(r'^api/docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', lambda request: redirect('api/docs/', permanent=False)),  # Redirect root to API docs
    # path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
]
