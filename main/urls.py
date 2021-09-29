from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.index, name="index"),
    path('staff', views.staffs_view, name="staffs"),
    path('departments', views.departments_view, name="departments"),
    path('departments/<int:id>', views.department_view, name="department"),
    path('staff/<int:id>', views.delete_staff_view, name="delete"),
    path('staff/create', views.staff_view, name="staff"),
    path('successful/<str:data>', views.success_view, name="success"),
    path('accounts/login/', views.login_view, name="login"),
    path('accounts/register', views.register_view, name="register"),
    path('accounts/logout', views.logout_view, name="logout")
]