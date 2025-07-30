"""Views."""

from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.shortcuts import render

from .utils.geospatial import Geospatial


@login_required
@permission_required("evemap.basic_access")
def index(request):
    """Render index view."""

    context = {"text": "Hello, World!"}
    return render(request, "evemap/index.html", context)


@login_required
@permission_required("evemap.basic_access")
def geospatial(request, layer: str):

    return JsonResponse(Geospatial.layer(layer))
