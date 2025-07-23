"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.urls import include
from login import views
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from login.views import HelloView
from login.views import UserListView

urlpatterns = [

]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('login/', views.login),
    path('logout/', views.logout),
    path('register/', views.register),
    path('captcha', include('captcha.urls')),
    path('confirm/', views.user_confirm),
    path('api/users/', UserListView.as_view(), name='user-list'),
    path('api/hello/', HelloView.as_view(), name='hello'),
    # 文档路由
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # ReDoc UI
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
