from django.contrib import admin
from .models import (
    Country,
    PointCompany,
    Truck,
    Trailer,
    Driver,
    Task,
    Customer,
    Order,
    TaskType,
    CustomerManager,
    TaskStatus,
    TaskStatusChange,
    PaymentType,
    Point,
    OrderFile,
    FileType,
    Platform,
    DriverAssignment,
    TrailerAssignment,

)

# Register your models here.
admin.site.register(Country)
admin.site.register(PointCompany)

admin.site.register(Trailer)
admin.site.register(Driver)
admin.site.register(PaymentType)
admin.site.register(Customer)
admin.site.register(CustomerManager)
admin.site.register(TaskType)
admin.site.register(TaskStatus)
admin.site.register(OrderFile)
admin.site.register(FileType)
admin.site.register(Platform)
admin.site.register(DriverAssignment)
admin.site.register(TrailerAssignment)


class TaskStatusChangeAdmin(admin.ModelAdmin):
    list_display = [
        "task",
        "status",
        "start_date",
        "start_time",
        "end_date",
        "end_time",
        "is_active",
    ]
    #   fields = ['task', 'status', 'start_date', 'start_time', 'end_date', 'end_time', 'is_active']
    readonly_fields = ["start_date", "start_time"]


admin.site.register(TaskStatusChange, TaskStatusChangeAdmin)


class PointAdmin(admin.ModelAdmin):
    readonly_fields = ["id"]
    list_display = [
        "id",
        "postal_code",
        "country",
        "city",
        "street",
        "street_number",
        "gps_latitude",
        "gps_longitude",
        "company_name",
        "customer",
        "created_at",
    ]


admin.site.register(Point, PointAdmin)


class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ["id"]
    list_display = ["id", "type", "title", "truck", "driver", "order",  "point", "status"]


admin.site.register(Task, TaskAdmin)

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ["id"]
    list_display = ["id", "user", "number", "order_number", "price", "payment_type", "customer", "customer_manager", "created_at", "rout", "distance", "cargo_name", "cargo_weight", "loading_type", "trailer_type"]


admin.site.register(Order, OrderAdmin)


class TruckAdmin(admin.ModelAdmin):
    readonly_fields = ["id"]
    list_display = ["id", "plates", "model", "trailer", "driver_profile"]

admin.site.register(Truck, TruckAdmin)