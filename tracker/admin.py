# tracker/admin.py
from django.contrib import admin
from .models import User, Spent, Earned, Investments

# Show your custom User in admin (with balance and phone)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phonenumber', 'balance')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('balance',)   # balance will be updated by code, not manually


# Register the three transaction models
admin.site.register(Spent)
admin.site.register(Earned)
admin.site.register(Investments)