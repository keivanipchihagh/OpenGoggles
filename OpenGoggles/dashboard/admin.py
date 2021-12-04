from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    
    list_display = ['first_name', 'last_name', 'username', 'email_address', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['email_address']