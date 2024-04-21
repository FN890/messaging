"""
URL configuration for messaging project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path
from rest_framework import routers
from messaging.app import views


router = routers.DefaultRouter()

api_version = "api/v1/"

urlpatterns = [
    path('', include(router.urls)),
    path(api_version + "get-users/", views.GetUsers.as_view(), name="get-users"),
    path(api_version + "post-users/", views.PostUser.as_view(), name="post-users"),
    path(api_version + "delete-users/", views.DeleteUser.as_view(), name="delete-users"),
    path(api_version + "get-messages/<int:user_id>/<str:last_update>/", views.GetNewMessages.as_view(), name="get-messages-last-update"),
    path(api_version + "get-messages/<int:user_id>/<int:start_index>/<int:end_index>/", views.GetMessagesByIndices.as_view(), name="get-messages-indices"),
    path(api_version + "post-message/", views.PostMessage.as_view(), name="post-message"),
    path(api_version + "delete-messages/", views.DeleteMessages.as_view(), name="delete-messages"),
    path("admin/", admin.site.urls),
]