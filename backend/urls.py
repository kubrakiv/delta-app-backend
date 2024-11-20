from django.contrib import admin
from django.urls import path, re_path, include

from django.conf import settings # it's access to variables in settings.py file
from django.conf.urls.static import static # it's a specific function that connects urls
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", TemplateView.as_view(template_name="index.html")),
    path("api/csrf-token/", include("base.urls.csrf_token_urls")),
    path("api/orders/", include("base.urls.order_urls")),
    path("api/tasks/", include("base.urls.task_urls")),
    path("api/points/", include("base.urls.point_urls")),
    path("api/trucks/", include("base.urls.truck_urls")),
    path("api/trailers/", include("base.urls.trailer_urls")),
    path("api/customers/", include("base.urls.customer_urls")),
    path("api/customer-managers/", include("base.urls.customer_manager_urls")),
    path("api/point-companies/", include("base.urls.point_company_urls")),
    path("api/countries/", include("base.urls.country_urls")),
    path("api/documents/", include("base.urls.upload_documents_urls")),
    path("api/file-types/", include("base.urls.file_types_urls")),
    path("api/platforms/", include("base.urls.platform_urls")),
    path("api/payment-types/", include("base.urls.payment_types_urls")),
    path("api/task-types/", include("base.urls.task_types_urls")),
    path("api/send-email/", include("base.urls.send_email_urls")),
    path("api/company/", include("base.urls.company_urls")),
    path("api/currencies/", include("base.urls.currency_urls")),
    path("api/invoices/", include("base.urls.invoice_urls")),
    
    path("api/roles/", include("user.urls.role_urls")),
    path("api/users/", include("user.urls.user_urls")),
    path("api/driver-profiles/", include("user.urls.driver_profile_urls")),

    # Catch-all URL pattern for React app
    # re_path(r'^.*$', TemplateView.as_view(template_name="index.html")),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
