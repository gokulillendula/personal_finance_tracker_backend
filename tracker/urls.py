from django.urls import path,include
from .views import greet,user_login,spent,Earned,UserSummary,Users



urlpatterns = [
    path('greet/',greet,name='greet'),
    path('users/',Users.as_view(),name='users'),
    path('register/',Users.as_view(),name='register'),
    path('login/',user_login,name='user_login'),
    path('user/dashboard/',UserSummary.as_view(),name='dashboard'),
    path('user/spent/',spent.as_view(),name='addSpent'),
    path('user/earned/',Earned.as_view(),name='add_money'),
]