from django.conf import settings

def site_settings(request):
    return {
        'SITE_NAME': 'Deposits Platform',
        'SITE_DESCRIPTION': 'Enterprise Smart Storage & Courier Management',
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
        'CURRENT_YEAR': 2026,
        'VAT_PERCENTAGE': settings.VAT_PERCENTAGE,
    }
