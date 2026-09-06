from django.urls import path, re_path
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

def home_view(request):
    return render(request, 'shared/home.html')

@login_required
def dashboard_view(request):
    user = request.user
    template_map = {
        'ADMIN': 'admin/dashboard.html',
        'MANAGER': 'admin/dashboard.html',
        'COURIER': 'courier/dashboard.html',
        'WAREHOUSE': 'warehouse/dashboard.html',
        'CUSTOMER': 'customer/dashboard.html',
    }
    template = template_map.get(user.user_type, 'customer/dashboard.html')
    return render(request, template)

customer_templates = {
    'new-request': 'customer/new_request.html',
    'my-requests': 'customer/my_requests.html',
    'request-detail': 'customer/request_detail.html',
    'payments': 'customer/payments.html',
    'tickets': 'customer/tickets.html',
    'profile': 'customer/profile.html',
}

@login_required
def customer_view(request, page):
    template = customer_templates.get(page, 'customer/dashboard.html')
    return render(request, template)

urlpatterns = [
    path('', home_view, name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]

for page_name in customer_templates:
    urlpatterns.append(
        path(f'customer/{page_name}/', customer_view, {'page': page_name}, name=f'customer-{page_name}')
    )
