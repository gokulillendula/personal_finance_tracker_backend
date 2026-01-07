from django.urls import path,include
from .views import greet,register,user_login,dashboard,Addspent,UserList,AddEarned



urlpatterns = [
    path('greet/',greet,name='greet'),
    path('users/',UserList.as_view(),name='users'),
    path('register/',register,name='register'),
    path('login/',user_login,name='user_login'),
    path('dashboard/',dashboard,name='dashboard'),
    path('addSpent/',Addspent.as_view(),name='addSpent'),
   # path('login/',login_view,name='login'),
    #path('dashboard/',dashboard,name='dashboard'),
    path('add_money/',AddEarned.as_view(),name='add_money'),
]