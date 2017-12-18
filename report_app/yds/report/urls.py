from django.urls import path
from . import views


app_name = "report"


urlpatterns = [
        # Home page.
        path('', views.index, name='index'),

        # ex : /Attiki/
        path('<str:a_region>/', views.selected_region, name='selected_region'),

        # ex : /Attiki/N. ANATOLIKIS ATTIKIS"
        path('<str:a_region>/<str:a_municipality>/', views.selected_municipality, name='selected_municipality'),
    ]
