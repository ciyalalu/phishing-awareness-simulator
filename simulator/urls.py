from django.urls import path
from . import views

urlpatterns = [
    path('account-verify/', views.login_view, name='login'),
    path('warning/', views.warning_view, name='warning'),
    path('soc-dashboard/', views.soc_dashboard, name='soc'),
    path('delete-log/<int:log_id>/', views.delete_log, name='delete_log'),
]
