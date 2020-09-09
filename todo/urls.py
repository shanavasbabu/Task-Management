from django.contrib import admin
from django.urls import path
from . import views
# from .views import UserEditView, PasswordsChangeView
# from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    # path('password/', auth_views.PasswordChangeView.as_view(template_name='todo/change_password.html')),
    # path('password/', PasswordsChangeView.as_view(template_name='todo/change_password.html')),
    # path('password_success', views.password_success, name='password_success'),

    # Todos
    path('current/', views.currenttodos, name='currenttodos'),
    path('', views.home, name='home'),
    path('create/', views.createtodo, name='createtodo'),
    path('todo/<int:todo_pk>', views.viewtodo, name='viewtodo'),
    path('todo/<int:todo_pk>/complete', views.completetodo, name='completetodo'),
    path('todo/<int:todo_pk>/delete', views.deletetodo, name='deletetodo'),
    path('completed/', views.completedtodos, name='completedtodos'),
    path('profile_1/', views.view_profile, name='profile_1'),
    # path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
]
