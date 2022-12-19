from django.core.exceptions import FieldDoesNotExist, BadRequest, PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.http import FileResponse
from . import models
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from .serializers import FileSerializer
import mimetypes

def response_code(code: int):
    response =  HttpResponse(status=code)
    response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    response['Access-Control-Allow-Credentials'] = 'true'
    return response

@csrf_protect
def save_file(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            name = request.POST['name']
            file = request.POST['file']
            #faire des check de validité
            new_file = models.File.objects.create(request.user, name, file)
            new_file.save()
            return response_code(200)
        else:
            print("user not log")
            raise PermissionDenied()
    raise BadRequest()

class HasFileAccesPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return False
        return True

@api_view(['GET'])
def get_file_by_id(request, file_id):
    file = models.File.objects.get(pk=file_id)
    if file.owner != request.user:
        raise PermissionDenied('Not Access')
    serializer = FileSerializer(instance=file)
    return Response(serializer.data, 200)
        
@csrf_protect
def get_files_name(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            file_list : list = models.File.objects.filter(owner=request.user).all()
            responses = []
            for file in file_list:
                file_location = file.file.path
                with open(file_location, 'rb') as f:
                    content_type, _ = mimetypes.guess_type(file.file.name)
                    file_data = f.read()
                    response = HttpResponse(file_data, content_type=content_type)
                    response['Content-Disposition'] = f'attachment; filename="{file.name}"'
                    return response
            return HttpResponse(responses)

        raise PermissionDenied()
    raise BadRequest()

@csrf_protect
def update_file(request):
    if request.user.is_authenticated:
        file_list : list = list(models.File.objects.filter(owner=request.user))
        if (len(file_list) == 0):
            raise FieldDoesNotExist()
        file_id = request.POST['id']
        new_name = request.POST['name']
        new_file = request.POST['file']
        for file in file_list:
            if file.pk == file_id:
                if (new_name != None):
                    file.name = new_name
                if (new_file != None):
                    file.file = new_file
                file.save()
                response_data = {
                    'data': file,
                }
                return JsonResponse(response_data, headers={
                    'Access-Control-Allow-Origin': 'http://localhost:3000',
                    'Access-Control-Allow-Credentials': 'true'
                })
        raise FieldDoesNotExist()
    else:
        raise PermissionDenied()