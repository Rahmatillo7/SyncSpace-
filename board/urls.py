# boardapp/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Auth
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # Dashboard
    path('dashboard/', views.dashboards, name='dashboard'),

    # Board
    path('board/create/', views.create_board, name='create_board'),
    path('board/<slug:slug>/', views.board_detail, name='board_detail'),
    path('whiteboard/<slug:slug>/', views.whiteboard_detail, name='whiteboard_detail'),
]