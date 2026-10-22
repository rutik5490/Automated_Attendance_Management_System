from django.contrib import admin
from .models import WhatsAppMessage

# Register your models here.

class WhatsAppMessageAdmin(admin.ModelAdmin):
    list_display = ('student', 'message', 'sent_at', 'is_delivered')
    search_fields = ('student__name', 'message')
    list_filter = ('is_delivered', 'sent_at')
    date_hierarchy = 'sent_at'
    readonly_fields = ('sent_at',)

admin.site.register(WhatsAppMessage, WhatsAppMessageAdmin)