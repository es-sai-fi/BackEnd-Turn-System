from django.contrib.auth.views import LoginView
from django.urls import path
from .views import user_api_view, user_detail, Login, Logout, user_employee_api_view


urlpatterns = [
    path('', user_api_view, name='user_api'),
    path('employee',user_employee_api_view, name='employee_api'),
    path('<int:uid>', user_detail, name='user_detail'),
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
]
