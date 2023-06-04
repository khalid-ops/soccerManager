from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('user-register',  views.user_registration),
    path('user-login',  views.user_login),
    path('user-logout', views.user_logout),
    path('get-teams-data', views.get_users_teams_details),
    path('update-teams', views.update_teams_data),
    path('update-players', views.update_players_data),
    path('transfer-players', views.transfer_players),
    path('get/market-players', views.get_market_players),
    path('buy/players', views.to_buy_player)
]