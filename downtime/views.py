import json
from datetime import datetime  # Импортируем класс datetime из модуля datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse
from settings_app.models import LineSettings
from .models import Table
from django.views.decorators.csrf import csrf_exempt
from settings_app.models import DowntimeReason,Department,Section  # Не забудьте импортировать вашу модель

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone

from django.http import JsonResponse
from django.views import View
from .models import Speed

from django.http import JsonResponse
from django.views import View
from .models import Speed
from django.db.models import Q


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ProductOutput
from .serializers import ProductOutputSerializer

def get_lines(request):
    # Получаем уникальные номера линий из базы данных
    lines = Speed.objects.values_list('line', flat=True).distinct()
    
    # Преобразуем числа в строковые ключи в формате "line_X"
    formatted_lines = [f"line_{line}" for line in lines]
    
    # Возвращаем список линий в формате JSON
    return JsonResponse({'lines': formatted_lines})

class SpeedChartDataView(View):
    def get(self, request, *args, **kwargs):
        try:
            # Получаем уникальные номера линий
            lines = Speed.objects.values('line').distinct()

            # Словарь для хранения данных по каждой линии
            chart_data = {}

            for line in lines:
                line_number = line['line']
                
                # Получаем записи для каждой линии
                speeds = Speed.objects.filter(line=line_number)

                # Формируем метки времени для линии
                labels = [speed.time.strftime("%H:%M") for speed in speeds]  # Преобразуем время в формат HH:MM

                # Формируем значения скорости для этой линии
                values = [speed.speed for speed in speeds]

                # Добавляем данные для этой линии в словарь
                chart_data[f'line_{line_number}'] = {
                    'labels': labels,
                    'values': values
                }

            # Возвращаем данные в формате JSON
            return JsonResponse(chart_data)

        except Exception as e:
            # В случае ошибки отправляем сообщение
            return JsonResponse({"error": str(e)}, status=500)






def dashboard_view(request):
    # Данные для графиков

    active_lines = LineSettings.objects.filter(is_active=True)
    departments = Department.objects.all()  # Получаем все подразделения
    sections = Section.objects.all()

    return render(request, 'downtime/dashboard.html', {
        'lines': active_lines,
        'departments': departments,  
        "sections":sections,
    })


def active_lines_list(request):
    # Фильтруем только активные линии
    
    return render(request, 'settings_app/active_lines_list.html', {})



from django.http import JsonResponse
from datetime import datetime
from .models import Table  # Замените на свою модель, если она отличается

def downtime_details(request, line_number):
    try:
        # Получаем данные о простоях для указанной линии и текущей даты
        downtimes = Table.objects.filter(
            line=line_number, startdata=datetime.now().date()
        ).values('id', 'starttime', 'prostoy','uchastok', 'otv_pod', 'prichina', 'comment')

        # Возвращаем данные и информацию о том, авторизован ли пользователь
        return JsonResponse({
            'downtimes': list(downtimes),
            'is_authenticated': request.user.is_authenticated
        })

    except Table.DoesNotExist:
        # Обработка исключения, если нет данных для данной линии
        return JsonResponse({'downtimes': [], 'error': 'Line not found'})

    except Exception as e:
        # Обработка других ошибок
        return JsonResponse({'downtimes': [], 'error': str(e)})



@csrf_exempt  
def add_downtime(request):
    if request.method == 'POST':
                    

        try:
            data = json.loads(request.body)
            # Извлечение данных из запроса
            line = data.get('line')
            start_time_str = data.get('start_time')  # Время начала в строковом формате
            end_time_str = data.get('end_time') # Время окончания в строковом формате
            uchastok = data.get('uchastok')
            department = data.get('department')
            reason = data.get('responsible_unit')
            comment = data.get('comment')

            # Преобразование строк в объекты времени
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.strptime(end_time_str, '%H:%M').time()

            # Преобразование объектов времени в datetime для вычитания
            # Используем произвольную дату, так как нас интересует только время
            start_datetime = datetime.combine(datetime.today(), start_time)
            end_datetime = datetime.combine(datetime.today(), end_time)
            # Вычитание времени
            duration = end_datetime - start_datetime
            # Создание нового экземпляра модели Table
            downtime_entry = Table(
                startdata=timezone.now().date(),  # Устанавливаем сегодняшнюю дату
                starttime=start_time_str,               # Используем полученное время
                prostoy=str(duration),
                line=line,
                prichina=reason,
                otv_pod=department,
                uchastok = uchastok,
                comment=comment,
            )
            downtime_entry.save()  # Сохранение данных в базе
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Неверный метод'}, status=405)





@csrf_exempt
def update_downtime(request, id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            downtime = Table.objects.get(id=id)
            downtime.uchastok = data.get('uchastok', downtime.uchastok)
            downtime.otv_pod = data.get('otv_pod', downtime.otv_pod)
            downtime.prichina = data.get('prichina', downtime.prichina)
            downtime.comment = data.get('comment', downtime.comment)
            downtime.save() 
            return JsonResponse({"success": True})
        except Table.DoesNotExist:
            return JsonResponse({"success": False, "error": "Запись не найдена"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Неверный метод запроса"})



def get_departments(request):
    departments = Department.objects.values("id", "name")
    return JsonResponse(list(departments), safe=False)


def get_reasons(request, department_id):
    reasons = DowntimeReason.objects.filter(department_id=department_id).values('id', 'reason')
    return JsonResponse(list(reasons), safe=False)


def get_sections(request, line_id):
    line = LineSettings.objects.get(line_name=line_id)  # Находим объект
    line_id = line.id

    sections = Section.objects.filter(line_id=line_id, is_active=True).values('id', 'name')
    return JsonResponse(list(sections), safe=False)

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
import json
from .models import Table
from django.utils import timezone


@method_decorator(csrf_exempt, name='dispatch')
class StartProstoyView(View):
    def post(self, request, *args, **kwargs):
        try:
            # Получаем данные из тела запроса
            data = json.loads(request.body.decode('utf-8'))
            
            # Извлекаем необходимые данные
            line = data.get('line')


            # Проверяем, что данные обязательные есть
            if not line:
                return JsonResponse({"error": "Line number is required"}, status=400)

            # Создаем запись о простое
            prostoy_record = Table(
                line=line,
                startdata=timezone.now().date(),  # Устанавливаем текущую дату
                starttime=timezone.localtime(timezone.now()).time()  # Устанавливаем текущее время
            )
            prostoy_record.save()

            # Возвращаем успешный ответ
            return JsonResponse({"message": "Простой успешно записан"}, status=201)

        except Exception as e:
            # В случае ошибки отправляем сообщение
            return JsonResponse({"error": str(e)}, status=400)
        

from datetime import datetime, timedelta
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Table
from django.utils import timezone
import json


@method_decorator(csrf_exempt, name='dispatch')
class EndProstoyView(View):
    def post(self, request, *args, **kwargs):
        try:
            # Получаем данные из тела запроса
            data = json.loads(request.body.decode('utf-8'))

            # Извлекаем номер линии
            line = data.get('line')

            # Проверяем, что номер линии указан
            if not line:
                return JsonResponse({"error": "Line number is required"}, status=400)

            # Находим последнюю запись для данной линии
            last_record = Table.objects.filter(line=line).order_by('-id').first()

            if not last_record:
                return JsonResponse({"error": "No active prostoy found for the specified line"}, status=404)

            # Рассчитываем время простоя
            now = timezone.localtime(timezone.now())
            start_datetime = timezone.make_aware(
                datetime.combine(last_record.startdata, last_record.starttime)
            )
            prostoy_duration = now - start_datetime

            # Обновляем запись
            last_record.prostoy = (datetime.min + prostoy_duration).time()  # Сохраняем только время
            last_record.save()

            # Возвращаем успешный ответ
            return JsonResponse({
                "message": "Простой завершён",
                "duration": str(prostoy_duration)
            }, status=200)

        except Exception as e:
            # В случае ошибки отправляем сообщение
            return JsonResponse({"error": str(e)}, status=400)

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import localtime, now
import json
from .models import Speed
import pytz
@method_decorator(csrf_exempt, name='dispatch')
class RecordSpeedView(View):
    def post(self, request, *args, **kwargs):
        try:
            # Парсим тело запроса
            data = json.loads(request.body.decode('utf-8'))
            
            # Извлекаем данные из запроса
            line = data.get('line')
            speed = data.get('speed')
            
            # Проверка обязательных полей
            if line is None or speed is None:
                return JsonResponse({"error": "Line and speed are required"}, status=400)
            
            # Получаем текущее время в UTC
            utc_time = timezone.now()

            # Переводим в локальное время (например, Московское время)
            moscow_time = localtime(utc_time, timezone=pytz.timezone('Europe/Moscow'))

            # Записываем данные
            record = Speed(
                data=moscow_time.date(),
                time=moscow_time.time(),
                line=line,
                speed=speed
            )
            record.save()
            
            return JsonResponse({"message": "Data recorded successfully"}, status=201)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
        
        



class ProductOutputAPIView(APIView):
    def post(self, request):
        # Добавляем текущие дату и время в запрос
        data = request.data.copy()
        
                # Получаем текущее время в UTC
        utc_time = timezone.now()

        # Переводим в локальное время (например, Московское время)
        moscow_time = localtime(utc_time, timezone=pytz.timezone('Europe/Moscow'))

        # Записываем данные

        data['date'] = moscow_time.date()  # Текущая дата
        data['time'] = moscow_time.time()  # Текущее время

        serializer = ProductOutputSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Запись успешно добавлена', 'data': serializer.data}, 
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'message': 'Ошибка валидации', 'errors': serializer.errors}, 
            status=status.HTTP_400_BAD_REQUEST
        )
from django.http import JsonResponse
from django.db.models import Sum
from .models import ProductOutput

def product_quantity_chart(request):
    # Получаем данные о суммарном количестве продукции для каждой линии
    quantities = ProductOutput.objects.values('line').annotate(total_quantity=Sum('quantity'))

    # Подготовка данных
    data = {
        'lines': [f"Линия {entry['line']}" for entry in quantities],
        'quantities': [entry['total_quantity'] for entry in quantities]
    }
    return JsonResponse(data)

