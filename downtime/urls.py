from django.urls import path
from .views import *
urlpatterns = [
    path('', dashboard_view, name='dashboard_view'),
    path('downtime_details/<int:line_number>/', downtime_details, name='downtime_details'),
    path('add_downtime/', add_downtime, name='add_downtime'),

    path('api/reasons/<int:department_id>/', get_reasons, name='get_reasons'),
    path('update_downtime/<int:id>/', update_downtime, name='update_downtime'),
    path('get_departments/', get_departments, name='get_departments'),

    path('api/start_prostoy/', StartProstoyView.as_view(), name='start_prostoy'),
    path('api/end_prostoy/', EndProstoyView.as_view(), name='end_prostoy'),  # URL для завершения простоя
    path('api/record_speed/', RecordSpeedView.as_view(), name='record_speed'),
    path('api/get_speed_data/', SpeedChartDataView.as_view(), name='get_speed_data'),
    path('api/get_lines', get_lines, name='get_lines'),

    path('api/section/<int:line_id>/', get_sections, name='get_sections'),
    path('product-quantity-chart/', product_quantity_chart, name='product_quantity_chart'),

    path('api/product-output/', ProductOutputAPIView.as_view(), name='product-output-api'),


]
 