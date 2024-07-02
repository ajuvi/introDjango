from django.urls import path

from . import views

# si no posem app_name no funcionen el links
# les urls dels links les fem a partir de polls:name
app_name = "lliga"

urlpatterns = [
    path("", views.IndexView, name="index"),
    path("menu", views.MenuView, name="menu"), 
    path("<int:lliga_id>/classificacio", views.ClassificacioView, name="classificacio"),    
]
