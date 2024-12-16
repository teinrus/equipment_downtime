from django import forms
from .models import LineSettings
from .models import Department
from .models import DowntimeReason 

class LineSettingsForm(forms.ModelForm):
    class Meta:
        model = LineSettings
        fields = ['line_name', 'is_active', 'fixation_time']

    def __init__(self, *args, **kwargs):
        super(LineSettingsForm, self).__init__(*args, **kwargs)  # исправлено порядок вызова
        # Добавляем классы к полям формы
        self.fields['line_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Выберите линию'
        })
        self.fields['is_active'].widget.attrs.update({
            'class': 'form-check-input'
        })
        self.fields['fixation_time'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите время фиксации (мин)'
        })

    def clean_line_name(self):
        line_name = self.cleaned_data.get('line_name')
        
        # Если объект редактируется (есть pk), то пропускаем проверку для текущего объекта
        if LineSettings.objects.filter(line_name=line_name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(f'Линия с таким именем уже существует.')
        
        return line_name



class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']  
        labels = {
            'name': 'Название подразделения',  
        }



class DowntimeReasonForm(forms.ModelForm):
    class Meta:
        model = DowntimeReason
        fields = ['department', 'reason']  
        labels = {
            'department': 'Подразделение',  
            'reason': 'Причина простоя',     
        }

