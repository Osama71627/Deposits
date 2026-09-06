from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

api_patterns = [
    path('accounts/', include('apps.accounts.urls')),
    path('customers/', include('apps.customers.urls')),
    path('couriers/', include('apps.couriers.urls')),
    path('warehouse/', include('apps.warehouse.urls')),
    path('fleet/', include('apps.fleet.urls')),
    path('assets/', include('apps.assets.urls')),
    path('accounting/', include('apps.accounting.urls')),
    path('crm/', include('apps.crm.urls')),
    path('hr/', include('apps.hr.urls')),
    path('payments/', include('apps.payments.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('analytics/', include('apps.analytics.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_patterns)),
    path('api-auth/', include('rest_framework.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('', include('apps.accounts.web_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
