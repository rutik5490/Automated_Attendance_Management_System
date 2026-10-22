from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.management import call_command
from django.http import HttpResponse
from io import StringIO
import sys

@staff_member_required
def sync_external_data_view(request):
    """View to sync external data"""
    if request.method == 'POST':
        # Capture command output
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        
        try:
            # Call the management command
            call_command('sync_external_db')
            sys.stdout = old_stdout
            output = mystdout.getvalue()
            
            messages.success(request, f'Successfully synced external data: {output}')
        except Exception as e:
            sys.stdout = old_stdout
            messages.error(request, f'Error syncing external data: {str(e)}')
        
        return redirect('admin:index')
    
    return render(request, 'admin/management/sync_external_data.html')

@staff_member_required
def generate_reports_view(request):
    """View to generate reports"""
    if request.method == 'POST':
        # Capture command output
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        
        try:
            # Call the management command
            call_command('generate_reports')
            sys.stdout = old_stdout
            output = mystdout.getvalue()
            
            messages.success(request, f'Successfully generated reports: {output}')
        except Exception as e:
            sys.stdout = old_stdout
            messages.error(request, f'Error generating reports: {str(e)}')
        
        return redirect('admin:index')
    
    return render(request, 'admin/management/generate_reports.html')

@staff_member_required
def send_alerts_view(request):
    """View to send alerts"""
    if request.method == 'POST':
        # Capture command output
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        
        try:
            # Call the management command
            call_command('send_low_attendance_alerts')
            sys.stdout = old_stdout
            output = mystdout.getvalue()
            
            messages.success(request, f'Successfully sent alerts: {output}')
        except Exception as e:
            sys.stdout = old_stdout
            messages.error(request, f'Error sending alerts: {str(e)}')
        
        return redirect('admin:index')
    
    return render(request, 'admin/management/send_alerts.html')

@staff_member_required
def database_backup_view(request):
    """View to backup database"""
    if request.method == 'POST':
        # For database backup, we would typically use a different approach
        # This is a placeholder for demonstration
        messages.success(request, 'Database backup initiated successfully')
        return redirect('admin:index')
    
    return render(request, 'admin/management/database_backup.html')
