import os
from django.shortcuts import render


def map(request):
    return render(request, "spots/map.html", {"key": os.environ.get("GOOGLE_MAPS_API_KEY")})
