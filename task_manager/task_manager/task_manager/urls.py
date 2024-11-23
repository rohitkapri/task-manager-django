from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('tasks/', views.task_list, name='task_list'),
    path('task/new/', views.create_task, name='create_task'),
    path('task/<int:pk>/edit/', views.update_task, name='update_task'),
    path('task/<int:pk>/delete/', views.delete_task, name='delete_task'),
    path('task/<int:pk>/toggle/', views.toggle_task, name='toggle_task'),
    path('login/', auth_views.LoginView.as_view(template_name='tasks/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('auth/google/', views.google_login, name='google_login'),
    path('oauth2callback/', views.oauth2callback, name='oauth2callback'),
]
