"""expenseTracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from rest_framework.routers import SimpleRouter

from api.v1.account.views import UserRegister, UserListView
from api.v1.group.views import GroupViewSet, MemberListView, MemberDeleteView
# from api.v1.group.views import GroupListView, GroupDetailView, MemberListView, MemberDeleteView
from api.v1.activity.views import ActivityViewSet, AccountView

router = SimpleRouter()
router.register("group", GroupViewSet, base_name='group')
router.register("activity", ActivityViewSet, base_name='activity')


urlpatterns = [
    path('account/login/', obtain_jwt_token),
    path('account/token-refresh/', refresh_jwt_token),
    path('account/token-verify/', verify_jwt_token),
    path('account/register/', UserRegister.as_view()),

    path('user/', UserListView.as_view()),

    # path('group/', GroupListView.as_view()),
    # path('group/<int:pk>/', GroupDetailView.as_view()),
    
    path('group/<int:gid>/member/', MemberListView.as_view()),
    path('group/<int:gid>/member/<int:mid>/', MemberDeleteView.as_view()),
    
    path('account/', AccountView.as_view()),
]

urlpatterns += router.urls