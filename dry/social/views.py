from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SpotAV


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

        spotAV.add_to_new_spot_page()

        return JsonResponse({})

    return JsonResponse({"error": "not post"})
