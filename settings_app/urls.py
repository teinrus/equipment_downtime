from django.urls import path
from . import views, views_sections


urlpatterns = [
    path('lines/', views.line_settings_list, name='line_settings_list'),
    path('lines/add/', views.add_line_settings, name='add_line_settings'),
    path('lines/edit/<int:pk>/', views.edit_line_settings, name='edit_line_settings'), 
    path('line/delete/<int:pk>/', views.delete_line_settings, name='delete_line_settings'),

    path('departments/', views.department_settings_list, name='department_settings_list'),
    path('departments/add/', views.add_department, name='add_department'),
    path('departments/edit/<int:pk>/', views.edit_department, name='edit_department'),  
    path('department/delete/<int:pk>/', views.delete_department, name='delete_department'),
  
    path('reason/', views.reason_settings_list, name='reason_settings_list'),
    path('reason/add/', views.add_downtime_reason, name='add_downtime_reason'),
    path('downtime_reasons/edit/<int:pk>/', views.edit_downtime_reason, name='edit_downtime_reason'),
    path('downtime_reason/delete/<int:pk>/', views.delete_downtime_reason, name='delete_downtime_reason'),

    path('sections/', views_sections.section_management, name='section_management'),
    path('sections/add/', views_sections.add_section, name='add_section'),
    path('sections/toggle/<int:section_id>/', views_sections.toggle_section, name='toggle_section'),
    path('sections/delete/<int:section_id>/', views_sections.delete_section, name='delete_section'),
    
    path('get_sections/<int:line_id>/', views_sections.get_sections, name='get_sections'),

    
]
