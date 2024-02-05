from . import views
from django.contrib.auth import views as auth_views
from django.urls import path
app_name='movieapp'

urlpatterns = [
    path('', views.home,name='home'),
    path('profile/', views.profile,name='profile'),
    path('', views.just_registered,name='just_registered'),
    # path('add/', views.add, name='add'),
    # path('register/', views.register, name='register'),
    # path('login/', views.login, name='login'),
    # path('add/', views.add, name='add'),
    # path('logout/', views.logout, name='logout'),
    path('movie/<int:movie_id>/', views.detail, name='detail'),
    path('add/', views.add, name='add'),
    path('update/<int:id>/', views.update, name='update'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('search/', views.search, name='search'),
    path('register/',views.register,name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<slug:c_slug>/',views.moviecat,name='movies_by_category'),
    path('<slug:c_slug>/<slug:movies_slug>/',views.movdetail,name='movcatdetail'),

    path('',views.moviecat,name='moviecat'),
    path('<slug:c_slug>/',views.moviecat,name='movies_by_category'),
]