from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .MyPackages import Microservices as ms


def index(request):
    return render(request, 'portfolio/index.html')

def timestamp(request, data: str = None):
    if data:
        return JsonResponse(ms.timestamp(data))
    title = "Timestamp Microservice"
    url = request.build_absolute_uri()
    return render(request, "portfolio/microservices/timestamp.html", locals())

def header(request, data: str = None):
    if data == "whoami":
        return JsonResponse(ms.parse_header(request))
    title = "Request Header Parser Microservice"
    url = request.build_absolute_uri()
    return render(request, "portfolio/microservices/header_parser.html", {"title": title, "url": url})

@csrf_exempt
def metadata(request):
    if request.method == "POST":
        return JsonResponse({"size": request.FILES.get('myfile').size})

    title = "File Metadata Microservice"
    url = request.build_absolute_uri()
    return render(request, "portfolio/microservices/file_metadata.html", {"title": title, "url": url})


