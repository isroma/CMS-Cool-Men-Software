from django.shortcuts import render
import json
import tika
from django.http import HttpResponse
from tika import parser

def index(request):
    return render(request, 'index.html')

def tika(request):
    if request.method == 'GET':
        
        # Para recibir en formato XHTML
        response_data = parser.from_file('/home/frias/sample.pdf', xmlContent=True)
        # Para recibir en texto plano
        # response_data = parser.from_file('/home/frias/sample.pdf')

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )