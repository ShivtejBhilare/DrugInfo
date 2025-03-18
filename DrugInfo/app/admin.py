from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app.models import CustomUser, Drug, Doctor, DrugDoctor

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Drug)
admin.site.register(Doctor)
admin.site.register(DrugDoctor)
