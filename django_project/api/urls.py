from django.urls import path, re_path
from . import views


urlpatterns = [
    path('api/getshorten/', views.generate_shorten, name='generate_shorten'),
    path('<str:unique_code>/', views.redirect),
    path('', views.main_page, name='main_page')
]

