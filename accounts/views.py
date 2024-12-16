# accounts/views.py
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import RegistrationForm
# в вашем файле views.py
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from .forms import EditProfileForm
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import EditUserForm  # Эта форма будет использоваться для редактирования пользователя
from accounts.models import CustomUser


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # Используем форму для аутентификации
        if form.is_valid():
            user = form.get_user()  # Получаем пользователя из формы
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему.')
            return redirect('dashboard_view')  # Перенаправление на главную страницу после успешного входа
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})  # Отображаем форму на странице входа


def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')  # Сообщение об успешном выходе
    return redirect('dashboard_view')  # Замените на ваш URL после выхода



def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Устанавливаем пароль
            user.save()  # Сохраняем пользователя в базе данных

            # Добавляем пользователя в группу на основе роли
            role = form.cleaned_data.get('role')
            group_name = None
            if role == 'admin':
                group_name = 'Администраторы'
            elif role == 'engineer':
                group_name = 'Инженеры'
            elif role == 'user':
                group_name = 'Пользователи'

            if group_name:
                group, created = Group.objects.get_or_create(name=group_name)
                user.groups.add(group)

            login(request, user)  # Входим в систему после регистрации
            messages.success(request, 'Вы успешно зарегистрированы.')  # Успешное сообщение
            return redirect('dashboard_view')  # Перенаправление на главную страницу
    else:
        form = RegistrationForm()
    return render(request, 'accounts/registration.html', {'form': form})  # Отображение страницы регистрации



class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'  # Укажите свой шаблон

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем группы пользователя в контекст
        user = self.request.user
        context['user_groups'] = user.groups.all() if user.is_authenticated else []
        return context



@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()  # Сохраняем пользователя с обновленной ролью
            messages.success(request, 'Ваш профиль успешно обновлён.')
            return redirect('profile')  # Перенаправление на страницу профиля
    else:
        form = EditProfileForm(instance=request.user)  # Загружаем текущие данные пользователя
    return render(request, 'accounts/edit_profile.html', {'form': form})





def is_admin(user):
    # Проверяем, состоит ли пользователь в группе "Администраторы"
        return user.is_authenticated and (
        user.groups.filter(name='Администраторы').exists()
    )


# Представление для списка пользователей (только для администраторов)
@login_required
@user_passes_test(is_admin)
def user_management(request):
    users = CustomUser.objects.all()  # Получаем всех пользователей
    return render(request, 'accounts/user_management.html', {'users': users})

from django.shortcuts import render, get_object_or_404, redirect
from .models import CustomUser
from .forms import EditProfileForm

@login_required
@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)  # Используем get_object_or_404 для безопасного получения пользователя

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)  # Передаем текущего пользователя в форму
        if form.is_valid():
            form.save()  # Сохраняем изменения
            messages.success(request, 'Профиль успешно обновлен.')
            return redirect('user_management')  # Перенаправляем на страницу с пользователями
    else:
        form = EditProfileForm(instance=user)  # Заполняем форму данными пользователя для редактирования

    return render(request, 'accounts/edit_user.html', {'form': form, 'user': user})


# Представление для удаления пользователя
@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, f'Пользователь {user.username} успешно удален!')
        return redirect('user_management')
    return render(request, 'accounts/delete_user.html', {'user': user})
