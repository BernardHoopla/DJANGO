# example/urls.py
from django.template.defaulttags import url
# from django.conf.urls import include, url
from django.urls import path, include

from example import views  # import index


urlpatterns = [
    # home_page, login, choose_session, session (question, result)
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('start_session', views.choose_session, name='start_session'),
    path('session', views.session_view, name='session'),
    path('leaderboard', views.leaderboard_view, name='leaderboard'),
    path('toggle_leaderboard/', views.toggle_leaderboard, name='toggle_leaderboard'),
    # path('', views.index),
    # path(r"accounts/", include("django.contrib.auth.urls")),
    # login/ logout
    # path('input/', views.input_form, name='input_form'),
]