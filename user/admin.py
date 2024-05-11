from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User,
    Role,
    AdminProfile,
    LogistProfile,
    DriverProfile,
    # CustomerProfile
)

# Register your models here.
admin.site.register(Role)
admin.site.register(AdminProfile)
admin.site.register(LogistProfile)
admin.site.register(DriverProfile)
# admin.site.register(CustomerProfile)



fields = list(UserAdmin.fieldsets)
fields[1] = ('Personal Info', {'fields':('first_name','last_name', 'email', 'phone_number', 'role')})
UserAdmin.fieldsets = tuple(fields)
UserAdmin.list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'role')
admin.site.register(User, UserAdmin)


