from django.shortcuts import render, redirect, get_object_or_404
from .models import Section, LineSettings
from django.contrib import messages
from django.http import JsonResponse


# Управление участками
def section_management(request):
    lines = LineSettings.objects.prefetch_related('sections')
    return render(request, 'sections/section_management.html', {'lines': lines})

# Добавление нового участка
def add_section(request):
    if request.method == 'POST':
        line_id = request.POST.get('line')
        name = request.POST.get('name')

        line = get_object_or_404(LineSettings, id=line_id)
        Section.objects.create(name=name, line=line)
        messages.success(request, f"Участок '{name}' успешно добавлен к линии {line.get_line_name_display()}.")
        return redirect('section_management')

    lines = LineSettings.objects.all()
    return render(request, 'sections/add_section.html', {'lines': lines})

# Переключение активности участка
def toggle_section(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    section.is_active = not section.is_active
    section.save()
    messages.success(request, f"Статус участка '{section.name}' успешно изменен.")
    return redirect('section_management')

# Удаление участка
def delete_section(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    section.delete()
    messages.success(request, f"Участок '{section.name}' успешно удален.")
    return redirect('section_management')

def get_sections(request, line_id):

    line = LineSettings.objects.get(line_name=line_id)  # Находим объект
    line_id = line.id

    sections = Section.objects.filter(line_id=line_id, is_active=True).values('id', 'name')
    return JsonResponse(list(sections), safe=False)