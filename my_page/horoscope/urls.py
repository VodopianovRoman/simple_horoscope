from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='horoscope-index'),
    path('type', views.info_by_type),
    path('type/<str:sign_type>', views.get_info_by_type, name='horoscope-type'),
    path('<int:sign_zodiac>', views.get_info_about_sign_zodiac_by_number),
    path('<str:sign_zodiac>', views.get_info_about_sign_zodiac, name='horoscope-name'),
]

