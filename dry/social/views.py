from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SpotAV
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


# @api_view(['GET', 'POST'])
@csrf_exempt
def upload_spot_av(request):
    if request.method == 'POST':
        audio = request.FILES["audio"]
        image = request.FILES["image"]
        text = request.POST["text"]
        spotAV = SpotAV(audio=audio, image=image, text=text)
        spotAV.save()

        # form = UploadFileForm(request.POST, request.FILES)
        # files = request.FILES.getlist('file_field')
        # print(request.FILES)
        # for f in files:
        #    print(f)
        #    #instance = ModelWithFileField(file_field=request.FILES['file'])
        #    #instance.save()
        return JsonResponse({})

    return JsonResponse({"error": "not post"})
