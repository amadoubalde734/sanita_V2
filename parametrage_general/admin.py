from django.contrib import admin
from .models import EmailSettings

@admin.register(EmailSettings)
class EmailSettingsAdmin(admin.ModelAdmin):
    list_display = (
        'email_backend', 'email_host', 'email_port', 
        'email_use_tls', 'email_host_user', 'default_from_email'
    )
    fields = (
        'email_backend', 'email_host', 'email_port', 'email_use_tls',
        'email_host_user', 'email_host_password', 'default_from_email'
    )
