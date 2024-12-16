from django.shortcuts import render, redirect
from .models import LineSettings
from .forms import LineSettingsForm
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

def edit_line_settings(request, pk):
    line = get_object_or_404(LineSettings, pk=pk)  # Получаем объект линии по первичному ключу
    form = LineSettingsForm(instance=line)
    if request.method == 'POST':
        form = LineSettingsForm(request.POST, instance=line)
        if form.is_valid():
            form.save()
            return redirect('line_settings_list')  # Укажите имя вашего URL для перенаправления

    return render(request, 'settings_app/line/edit_line_settings.html',  {'form': form, 'line': line})

def is_engineer_or_admin(user):
    """Проверяет, является ли пользователь инженером или администратором."""
    return user.is_authenticated and (
        user.groups.filter(name='Инженеры').exists() or user.groups.filter(name='Администраторы').exists()
    )

@user_passes_test(is_engineer_or_admin, login_url='/accounts/login/')
def line_settings_list(request):
    lines = LineSettings.objects.all()
    return render(request, 'settings_app/line/line_settings_list.html', {'lines': lines})


def add_line_settings(request):
    if request.method == 'POST':
        form = LineSettingsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('line_settings_list')  
    else:
        form = LineSettingsForm()

    return render(request, 'settings_app/line/add_line_settings.html', {'form': form})

from django.shortcuts import get_object_or_404, redirect
from .models import LineSettings

def delete_line_settings(request, pk):
    line = get_object_or_404(LineSettings, pk=pk)
    print(line)
    if request.method == 'POST':
        line.delete()
        return redirect('line_settings_list')  # Укажите правильное имя для перенаправления

    return render(request, 'confirm_delete.html', {'line': line})  # Страница подтверждения удаления (опционально)


from django.shortcuts import render, redirect
from settings_app.models import Department, DowntimeReason  # Убедитесь, что ваши модели импортированы
from .forms import DepartmentForm, DowntimeReasonForm  # Импортируйте формы, если у вас есть


def department_settings_list(request):
    departments = Department.objects.all()  # Получаем все подразделения
    return render(request, 'settings_app/department/department_settings_list.html', {'departments': departments})

def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('line_settings_list')  # Перенаправление после успешного сохранения
    else:
        form = DepartmentForm()
    return render(request, 'settings_app/department/add_department.html', {'form': form})

def edit_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('department_settings_list')  # Перенаправление на список после сохранения
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'settings_app/department/edit_department.html', {'form': form})

def delete_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
    return redirect('department_settings_list')  # Перенаправление на список после удаления










def reason_settings_list(request):
    reasons = DowntimeReason.objects.all()  # Получаем все причины простоя
    return render(request, 'settings_app/department/department_reason_list.html', {'reasons': reasons})

def add_downtime_reason(request):
    if request.method == 'POST':
        department_id = request.POST.get('department')
        reason_text = request.POST.get('reason')
        
        # Найдите выбранное подразделение по ID
        department = Department.objects.get(pk=department_id)
        
        # Создайте новую причину простоя
        DowntimeReason.objects.create(department=department, reason=reason_text)
        
        return redirect('reason_settings_list')  # перенаправление на список причин

    departments = Department.objects.all()  # Получите все подразделения
    return render(request, 'settings_app/department/add_downtime_reason.html', {'departments': departments})

def edit_downtime_reason(request, pk):
    reason = get_object_or_404(DowntimeReason, pk=pk)

    if request.method == 'POST':
        form = DowntimeReasonForm(request.POST, instance=reason)
        if form.is_valid():
            form.save()
            return redirect('reason_settings_list')
    else:
        form = DowntimeReasonForm(instance=reason)

    return render(request, 'settings_app/department/edit_downtime_reason.html', {'form': form})

def delete_downtime_reason(request, pk):
    reason = get_object_or_404(DowntimeReason, pk=pk)
    if request.method == 'POST':
        reason.delete()

    return redirect('reason_settings_list')

