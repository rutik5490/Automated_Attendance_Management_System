from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from .models import User, Faculty, Dean, Student
import csv
import io

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('user_type', 'whatsapp_number')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('User Profile'), {'fields': ('user_type', 'whatsapp_number')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'user_type', 'whatsapp_number'),
        }),
    )
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('bulk-import/', self.admin_site.admin_view(self.bulk_import_view), name='users_user_bulk_import'),
        ]
        return custom_urls + urls
    
    def bulk_import_view(self, request):
        if request.method == 'POST':
            csv_file = request.FILES.get('csv_file')
            user_type = request.POST.get('user_type')
            
            if not csv_file:
                messages.error(request, 'Please select a CSV file to import.')
                return redirect('admin:users_user_bulk_import')
            
            if not user_type:
                messages.error(request, 'Please select a user type.')
                return redirect('admin:users_user_bulk_import')
            
            try:
                # Read CSV file
                decoded_file = csv_file.read().decode('utf-8')
                io_string = io.StringIO(decoded_file)
                reader = csv.DictReader(io_string)
                
                created_count = 0
                for row in reader:
                    # Extract fields
                    username = row.get('username')
                    email = row.get('email')
                    first_name = row.get('first_name', '')
                    last_name = row.get('last_name', '')
                    whatsapp_number = row.get('whatsapp_number', '')
                    
                    # Skip if user already exists
                    if User.objects.filter(username=username).exists():
                        continue
                    
                    # Create user
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password='default123',
                        first_name=first_name,
                        last_name=last_name,
                        user_type=user_type,
                        whatsapp_number=whatsapp_number
                    )
                    
                    # Create profile based on user type
                    if user_type == 'student':
                        Student.objects.create(
                            user=user,
                            name=f'{first_name} {last_name}',
                            roll_no=row.get('roll_no', ''),
                            whatsapp_number=whatsapp_number
                        )
                    elif user_type == 'faculty':
                        Faculty.objects.create(
                            user=user,
                            name=f'Prof. {first_name} {last_name}' if first_name else username
                        )
                    elif user_type == 'dean':
                        Dean.objects.create(
                            user=user,
                            name=f'Dr. {first_name} {last_name}' if first_name else username
                        )
                    
                    created_count += 1
                
                messages.success(request, f'Successfully imported {created_count} {user_type} users.')
                return redirect('admin:users_user_changelist')
                
            except Exception as e:
                messages.error(request, f'Error importing users: {str(e)}')
                return redirect('admin:users_user_bulk_import')
        
        context = {
            'title': 'Bulk Import Users',
            'site_title': 'Attendance Management System',
            'site_header': 'Attendance Management System',
            'has_permission': True,
        }
        return render(request, 'admin/users/bulk_import.html', context)

# Register other models
@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name', 'user__username')

@admin.register(Dean)
class DeanAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name', 'user__username')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'roll_no')
    search_fields = ('name', 'user__username', 'roll_no')