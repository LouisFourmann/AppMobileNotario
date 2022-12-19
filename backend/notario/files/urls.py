from django.urls import path

from . import views

app_name = 'files'

urlpatterns = [
    #path('/', views.save_file, name='save'), # POST
    path('', views.get_files_name, name='gets'), # GET
    path('<int:file_id>', views.get_file_by_id, name='get-file'), # GET id
    #path('/{id}', views.update_file, name='update'), # UPDATE id
]