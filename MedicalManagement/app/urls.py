from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('registration', views.registration, name='registration'),
    path('logout', views.logout, name='logout'),
    path('medicine', views.medicine, name='medicine'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('addmeds',views.addmeds,name='addmeds'),
    path('appointments',views.appointments,name='appointments'),
    path('handle_med_search', views.handle_med_search, name='handle_med_search'),
    path('handle_medicine', views.handle_medicine, name='handle_medicine'),
    path('handle_added_meds', views.handle_added_meds, name='handle_added_meds'),
    path('handle_registration', views.handle_registration, name='handle_registration'),
    path('handle_login', views.handle_login, name='handle_login'),
    path('handle_appointments',views.handle_appointments,name='handle_appointments'),
    path('handle_specialization',views.handle_specialization,name='handle_specialization'),
    path('handle_news',views.handle_news,name='handle_news'),
    path('handle_appointment_treated',views.handle_appointment_treated,name='handle_appointment_treated'),
]
