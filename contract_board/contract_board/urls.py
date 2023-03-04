"""contract_board URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path
from board import views as board_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', board_views.ContractListView.as_view(), name='home'),
    path('contract/new', board_views.ContractCreateView.as_view(), name='create_contract'),
    path('contract/<int:pk>', board_views.ContractDetailView.as_view()),
    path('contract/<int:pk>/bid', board_views.BidCreateView.as_view()),
    path('register', board_views.UserCreateView.as_view(), name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(next_page='home'), name='login'),
    path('user', board_views.UserView.as_view(), name='user')
]
