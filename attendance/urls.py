from django.urls import path
from . import views
from . import management_views

app_name = 'attendance'

urlpatterns = [
    path('upload-csv/', views.upload_attendance_csv, name='upload_attendance_csv'),
    path('generate-report/', views.generate_attendance_report, name='generate_attendance_report'),
    path('api/raspberry-pi/', views.RaspberryPiAttendanceView.as_view(), name='raspberry_pi_attendance'),
    # Management commands URLs
    path('management/sync-external-data/', management_views.sync_external_data_view, name='sync_external_data'),
    path('management/generate-reports/', management_views.generate_reports_view, name='generate_reports'),
    path('management/send-alerts/', management_views.send_alerts_view, name='send_alerts'),
    path('management/database-backup/', management_views.database_backup_view, name='database_backup'),
]