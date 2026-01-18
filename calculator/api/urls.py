from django.urls import path
from . import views

urlpatterns = [
    path("symbols/", views.symbols_api),
    path("calculate/", views.calculate_option_api),
    path("graphs/", views.graph_data_api),
    path("about/", views.about_api),
]
