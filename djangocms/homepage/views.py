from django.shortcuts import render
import json
import tika
from django.http import HttpResponse
from tika import parser

def index(request):
    return render(request, 'index.html')

def tika(request):
    if request.method == 'GET':
        
        # Receive tika data on XHTML format
        # response_data = parser.from_file('/home/frias/sample.pdf', xmlContent=True)
        # Receive tika data on plain text format
        response_data = parser.from_file('/home/frias/sample.pdf')

        # Cleaning of ends of line at the start of the plain text content received from Tika. DO NOT USE WITH XHTML FORMAT.
        response_data['content'] = re.sub('[\n]{1,}', '', response_data["content"], 1)

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )