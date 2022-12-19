from django.urls import path

from . import views

app_name = 'planning'

urlpatterns = [
    path('add/', views.AddEvent, name='add'), # POST
    path('<int:event_id>', views.UpdateEvent, name='update'), # POST / DELETE id
    path('', views.GetEvents, name='get_all'), # GET all
]