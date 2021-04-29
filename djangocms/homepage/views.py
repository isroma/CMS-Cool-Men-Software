import json
import tika
import hashlib
import hmac
import random
import string
import time
import uuid
import re

# TODO: clean trash

from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse
from django.template import RequestContext

from urllib.parse import urlparse
from swiftclient import client
from tika import parser
from .models import StorageObject

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

def random_key(length=20):
    chars = string.ascii_letters + string.digits
    return ''.join(random.SystemRandom().choice(chars) for _ in range(length))


def get_tempurl_key():
    (storage_url, auth_token) = client.get_auth(
        settings.SWIFT_AUTH_URL, settings.SWIFT_USER, settings.SWIFT_PASSWORD)

    try:
        meta = client.head_container(storage_url, auth_token,
                                     settings.SWIFT_CONTAINER)
        key = meta.get('x-container-meta-temp-url-key')
    except client.ClientException:
        client.put_container(storage_url, auth_token, settings.SWIFT_CONTAINER)
        key = None

    if not key:
        key = random_key()
        headers = {'x-container-meta-temp-url-key': key}
        client.post_container(storage_url, auth_token,
                              settings.SWIFT_CONTAINER, headers)

    return storage_url, key


def download(request, pk):
    so = StorageObject.objects.get(pk=pk)

    storage_url, key = get_tempurl_key()
    storage_url = storage_url.replace("swiftstack", "localhost")
    url = "%s/%s/%s" % (storage_url, so.container, so.objectname)

    expires = int(time.time() + 60)
    path = urlparse(url).path

    hmac_body = 'GET\n%s\n%s' % (expires, path)
    signature = hmac.new(bytearray(key.encode('utf-8')), hmac_body.encode('utf-8'), hashlib.sha1).hexdigest()
    signed_url = '%s?temp_url_sig=%s&temp_url_expires=%s' % (url, signature, expires)

    return redirect(signed_url)


def upload(request):
    storage_url, key = get_tempurl_key()
    storage_url = storage_url.replace("swiftstack", "localhost")
    prefix = str(uuid.uuid4())

    # In a real-world scenario you might want to record the prefix in a DB
    # before displaying the form to keep track of user uploads in case the
    # finalize() view is not called. Otherwise there will be data on Swift that
    # is not referenced within your application.
    # For example, run a periodic job that iterates over unused prefixes and
    # check Swift if there are unreferenced uploads

    max_file_size = 5*1024*1024
    max_file_count = 1
    expires = int(time.time() + 5*60)
    swift_url = "%s/%s/%s/" % (storage_url, settings.SWIFT_CONTAINER, prefix)
    redirect_url = "http://%s%s" % (request.get_host(), reverse(finalize, kwargs={'prefix': prefix}))
    path = urlparse(swift_url).path

    hmac_body = '%s\n%s\n%s\n%s\n%s' % (path, redirect_url, max_file_size, max_file_count, expires)
    signature = hmac.new(bytearray(key.encode('utf-8')), hmac_body.encode('utf-8'), hashlib.sha1).hexdigest()

    context = {
        'swift_url': swift_url, 'redirect_url': redirect_url,
        'max_file_size': max_file_size, 'max_file_count': max_file_count,
        'expires': expires, 'signature': signature
    }

    return render(request, 'upload.html', context)


def finalize(request, prefix):
    (storage_url, auth_token) = client.get_auth(settings.SWIFT_AUTH_URL, settings.SWIFT_USER, settings.SWIFT_PASSWORD)

    # Note: uploaded objects might not be listed yet due to the eventual
    # consistency. You might want to run an async job after some time to find
    # objects that are already uploaded, but not yet referenced in the DB.
    _meta, objects = client.get_container(storage_url, auth_token, settings.SWIFT_CONTAINER, prefix=prefix)

    # Remember DB ids. These are guessable, thus a real world app should use a
    # more sophisticated approach
    ids = []
    for obj in objects:
        dbentry, _created = StorageObject.objects.get_or_create(
            container=settings.SWIFT_CONTAINER,
            objectname=obj.get('name'),
            prefix=prefix)
        dbentry.save()
        ids.append(dbentry.id)

    return render(request, 'finalize.html', {'ids': ids, 'host': request.get_host()})
