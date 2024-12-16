from django.urls import path
from .views import login_view, logout_view, registration_view,edit_profile,user_management,edit_user,delete_user
from .views import ProfileView
urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', registration_view, name='register'), 
    path('profile/', ProfileView.as_view(), name='profile'), 
    path('profile/edit/', edit_profile, name='edit_profile'),  

    path('user_management/', user_management, name='user_management'),  # Список пользователей
    path('user_management/edit/<int:user_id>/', edit_user, name='edit_user'),  # Редактирование пользователя
    path('user_management/delete/<int:user_id>/', delete_user, name='delete_user'),  # Удаление пользователя


]
