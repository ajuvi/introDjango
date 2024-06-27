from django.urls import path

from . import views

# si no posem app_name no funcionen el links
# les urls dels links les fem a partir de polls:name
app_name = "polls"

urlpatterns = [
    path("", views.IndexView, name="index"),
    path("<int:question_id>/", views.DetailView, name="detail"),
    path("<int:question_id>/results/", views.ResultsView, name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]