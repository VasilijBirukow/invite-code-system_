from django.urls import path
from .views import auth_function, get_date_user, auth_page, main_page, profile_page, check_applied_code


urlpatterns = [
    path('', main_page),
    path('auth-page/', auth_page),
    path('auth/', auth_function),
    path('profile/', profile_page),
    path('user-data/', get_date_user),
    path('check-applied-code/', check_applied_code)
]
