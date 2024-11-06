from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import IntegerField
from django.db.models.functions import Cast, Substr, Length
from user.models import DriverProfile


# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=25)
    short_name = models.CharField(max_length=3)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class PointCompany(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Trailer(models.Model):
    plates = models.CharField(max_length=25)
    brand = models.CharField(max_length=50, null=True, blank=True)
    entry_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    vin_code = models.CharField(max_length=50, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    entry_mileage = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Trailer plates: {self.plates}"


class Truck(models.Model):
    plates = models.CharField(max_length=25)
    brand = models.CharField(max_length=50, null=True, blank=True)
    model = models.CharField(max_length=50, null=True, blank=True)
    entry_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    vin_code = models.CharField(max_length=50, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    entry_mileage = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    driver = models.ForeignKey(
        DriverProfile,
        related_name="trucks",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    trailer = models.ForeignKey(
        Trailer,
        related_name="trucks",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"Truck plates: {self.plates}"


class DriverAssignment(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    driver_profile = models.ForeignKey(DriverProfile, on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        start_date_str = self.start_date.strftime("%Y-%m-%d %H:%M") if self.start_date else "N/A"
        end_date_str = self.end_date.strftime("%Y-%m-%d %H:%M") if self.end_date else "present"
        return f"{self.driver_profile.full_name} assigned to {self.truck.plates} from {start_date_str} to {end_date_str}"


class TrailerAssignment(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    trailer = models.ForeignKey(Trailer, on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        start_date_str = self.start_date.strftime("%Y-%m-%d %H:%M") if self.start_date else "N/A"
        end_date_str = self.end_date.strftime("%Y-%m-%d %H:%M") if self.end_date else "present"
        return f"{self.trailer.plates} assigned to {self.truck.plates} from {start_date_str} to {end_date_str}"


class PaymentType(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Platform(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=50)
    nip_number = models.CharField(max_length=50, null=True, blank=True)
    payment_period = models.IntegerField(null=True, blank=True)
    payment_type = models.ForeignKey(
        PaymentType,
        related_name="customers",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    email = models.EmailField("Email Billing", max_length=255, null=True, blank=True)
    website = models.CharField(max_length=250, null=True, blank=True)
    post_address = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CustomerManager(models.Model):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    customer = models.ForeignKey(
        Customer,
        related_name="managers",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name + " " + self.customer.name


class Point(models.Model):
    country = models.ForeignKey(
        Country, related_name="points", on_delete=models.SET_NULL, null=True, blank=True
    )
    postal_code = models.CharField(max_length=6)
    city = models.CharField(max_length=25)
    street = models.CharField(max_length=255)
    street_number = models.CharField(max_length=5)
    gps_latitude = models.CharField(max_length=25)
    gps_longitude = models.CharField(max_length=25)
    company_name = models.ForeignKey(
        PointCompany,
        related_name="points",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    customer = models.ForeignKey(
        Customer,
        related_name="points",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Points"

    def __str__(self):
        if (
            self.customer
            and self.country
            and self.city
            and self.street
            and self.street_number
        ):
            return f"{self.customer.name}: {self.country.short_name}, {self.city}, {self.street}, {self.street_number}"
        else:
            return f"{self.id} {self.created_at}"


class Order(models.Model):
    number = models.CharField(max_length=20)  # auto-incremented number
    order_number = models.CharField(
        "Order number", max_length=20, null=True, blank=True
    )  # manual order number
    price = models.DecimalField(
        "Order price", max_digits=6, decimal_places=2, null=True, blank=True
    )
    market_price = models.DecimalField(
        "Market price", max_digits=6, decimal_places=2, null=True, blank=True
    )
    payment_type = models.ForeignKey(
        PaymentType,
        related_name="orders",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    payment_period = models.IntegerField(null=True, blank=True)
    rout = models.CharField(max_length=10, null=True, blank=True)
    distance = models.IntegerField(null=True, blank=True)
    cargo_name = models.CharField(max_length=50, null=True, blank=True)
    cargo_weight = models.CharField(max_length=50, null=True, blank=True)
    loading_type = models.CharField(max_length=50, null=True, blank=True)
    trailer_type = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="orders",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    platform = models.ForeignKey(
        Platform,
        related_name="orders",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    customer = models.ForeignKey(
        Customer,
        related_name="orders",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    customer_manager = models.ForeignKey(
        CustomerManager,
        related_name="orders",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    truck = models.ForeignKey(
        Truck, related_name="orders", on_delete=models.SET_NULL, null=True, blank=True
    )
    driver = models.ForeignKey(
        DriverProfile, related_name="orders", on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.number:
            # Calculate the auto-increasing number for the month
            current_month = timezone.now().month
            current_year = timezone.now().year

            last_order = (
                Order.objects.annotate(
                    number_int=Cast(
                        Substr("number", 1, Length("number") - 6), IntegerField()
                    )
                )
                .filter(
                    number__isnull=False,
                    created_at__month=current_month,
                    created_at__year=current_year,
                )
                .order_by("-number_int")
                .first()
            )

            if last_order:
                new_number = last_order.number_int + 1
            else:
                new_number = 1

            # Format the number field
            month_str = str(current_month).zfill(2)
            year_str = str(current_year)[-2:]
            self.number = f"{new_number}-{month_str}-{year_str}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order number: {self.number}, created at: {str(self.created_at)[0:19]}"


class FileType(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class OrderFile(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="order_files",
        on_delete=models.CASCADE
    )
    file_type = models.ForeignKey(
        FileType,
        related_name="file_type",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    file = models.FileField(upload_to='order_files/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_type.name} - File Name: {self.file.name[12:]}, Uploaded at: {str(self.uploaded_at)[0:19]}"


class TaskType(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TaskStatus(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Task Statuses"

    def __str__(self):
        return f"{self.id} - {self.name}"


class Task(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(auto_now_add=False, null=True, blank=True)
    start_time = models.TimeField(auto_now_add=False, null=True, blank=True)
    end_date = models.DateField(auto_now_add=False, null=True, blank=True)
    end_time = models.TimeField(auto_now_add=False, null=True, blank=True)
    order = models.ForeignKey(
        Order, related_name="tasks", on_delete=models.CASCADE, blank=True, null=True
    )
    point = models.ForeignKey(
        Point, related_name="tasks", on_delete=models.SET_NULL, blank=True, null=True
    )
    truck = models.ForeignKey(
        Truck, related_name="tasks", on_delete=models.CASCADE
    )
    driver = models.ForeignKey(
        DriverProfile, related_name="tasks", on_delete=models.CASCADE
    )
    type = models.ForeignKey(
        TaskType, related_name="tasks", on_delete=models.CASCADE
    )
    status = models.ForeignKey(
        TaskStatus,
        related_name="tasks",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.id}: {self.title}"

    def save(self, *args, **kwargs):
        # Flag to track if the task is new
        is_new = self._state.adding

        # Variables to hold previous status
        previous_status = None
        if not is_new:
            try:
                previous_status = self.__class__.objects.get(pk=self.pk).status
            except ObjectDoesNotExist:
                # Handle the case where the Task instance doesn't exist
                pass

        super().save(*args, **kwargs)  # Save the instance first

        # Check if the status has changed (only for existing tasks)
        if not is_new and self.status != previous_status:
            # Update the end_date and end_time for the last TaskStatusChange record
            last_status_change = self.status_changes.filter(
                end_date__isnull=True
            ).first()
            if last_status_change:
                last_status_change.end_date = timezone.now().date()
                last_status_change.end_time = timezone.now().time()
                last_status_change.is_active = False
                last_status_change.save()

            # Additional logic for specific status changes
            # (Adapt this part as per your application logic)
            if self.status.name == "Розвантаження завершено":
                last_loading_status_change = self.status_changes.filter(
                    status__name="Розвантаження завершено", end_date__isnull=True
                ).first()
                if last_loading_status_change:
                    last_loading_status_change.end_date = timezone.now().date()
                    last_loading_status_change.end_time = timezone.now().time()
                    last_loading_status_change.is_active = False
                    last_loading_status_change.save()

            # Create a new TaskStatusChange record for the new status
            TaskStatusChange.objects.create(task=self, status=self.status)


class TaskStatusChange(models.Model):
    task = models.ForeignKey(
        Task, related_name="status_changes", on_delete=models.CASCADE
    )
    status = models.ForeignKey(
        TaskStatus,
        related_name="status_changes",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    start_date = models.DateField(auto_now_add=True)
    start_time = models.TimeField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Task #{self.task.id}: {self.task.title} - {self.status.name} - {self.start_date} {self.start_time}"
