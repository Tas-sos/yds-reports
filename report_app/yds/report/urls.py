from django.urls import path
from . import views


app_name = "report"


urlpatterns = [
        # Home page.
        path('', views.index, name='index'),

        # About page.
        path('about/', views.about, name='about'),

        # ex : /Attiki/
        path('<str:a_region>/', views.selected_region, name='selected_region'),

        # ex : /Attiki/N. ANATOLIKIS ATTIKIS
        path('<str:a_region>/<str:a_municipality>/', views.selected_municipality, name='selected_municipality'),

        # ex: /Attiki/N. ANATOLIKIS ATTIKI/383752
        # path('<str:a_region>/<str:a_municipality>/<int:project_url_id>/', views.create_pdf, name='create_pdf'),

        # ex : /static/report/download/390273.pdf
        # path('static/report/download/<int:project_url_id>.pdf', views.create_pdf, name='create_pdf'),

        # ex : /pdf_error/Attiki/N. ANATOLIKIS ATTIKI/389383
        path('pdf_error/<str:a_region>/<str:a_municipality>/<int:project_url_id>/', views.pdf_error, name='pdf_error'),

        # ex : /ajax/create_pdf/389383
        path('ajax/create_pdf/<int:project_url_id>', views.create_pdf, name='create_pdf' ),

    ]
