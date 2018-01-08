from django.urls import path
from . import views


app_name = "report_api"


urlpatterns = [
    # ex : /api
    path('', views.all_regions, name='all_regions'),

    # ex : /api/Attiki/
    path('<str:a_region>/', views.all_municipalities, name='all_municipalities'),

    # ex : /api/Attiki/N. ANATOLIKIS ATTIKIS
    path('<str:a_region>/<str:a_municipality>/', views.all_projects, name='all_projects'),

    # ex : /api/Attiki/N. ANATOLIKIS ATTIKIS/525244
    path('<str:a_region>/<str:a_municipality>/<int:a_project>/', views.download_pdf, name='download_pdf'),

    # or ex : /api/Attiki/N. ANATOLIKIS ATTIKIS/http://linkedeconomy.org/resource/PublicWork/525244
    path('<str:a_region>/<str:a_municipality>/<path:a_project>/', views.redirect_to_download_pdf, name='redirect_to_download_pdf'),

]
