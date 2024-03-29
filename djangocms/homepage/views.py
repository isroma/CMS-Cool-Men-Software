import json
import tika
import hashlib
import hmac
import random
import string
import time
import uuid
import re

from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse
from urllib.parse import urlparse
from swiftclient import client
from tika import parser
from upload.models import StorageObject
from users.models import Role
from users.models import Profile
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import render
from users.models import Role, Profile

# Create your views here.

def index(request):

    if not request.user.is_authenticated:
        return redirect('/users/login')

    user = Profile.objects.get(user=request.user)
    roles = Role.objects.all()

    user = Profile.objects.get(user=request.user)
    roles = Role.objects.all()

    rol = request.GET.get('rol')

    storage_url, key, auth_token = get_tempurl_key(settings.SWIFT_CONTAINER)
    storage_url = storage_url.replace("swiftstack", "localhost")
    prefix = str(uuid.uuid4())

    # Creating dinamically containers according to Django roles
    (container_url, container_token) = client.get_auth(settings.SWIFT_AUTH_URL, settings.SWIFT_USER, settings.SWIFT_PASSWORD)

    headers = {'X-Container-Meta-Access-Control-Allow-Origin': '*', 'x-container-meta-temp-url-key': key}

    for role in roles:
        client.put_container(container_url, container_token, str(role))
        client.post_container(container_url, container_token, str(role), headers)

    # In a real-world scenario you might want to record the prefix in a DB
    # before displaying the form to keep track of user uploads in case the
    # finalize() view is not called. Otherwise there will be data on Swift that
    # is not referenced within your application.
    # For example, run a periodic job that iterates over unused prefixes and
    # check Swift if there are unreferenced uploads

    max_file_size = 5*1024*1024*1024
    max_file_count = 1
    expires = int(time.time() + 60*60*24*365)
    swift_url = "%s/%s/%s/" % (storage_url, settings.SWIFT_CONTAINER, prefix)
    redirect_url = "http://%s%s" % (request.get_host(), reverse(finalize, kwargs={'prefix': prefix, 'container': settings.SWIFT_CONTAINER}))
    path = urlparse(swift_url).path

    hmac_body = '%s\n%s\n%s\n%s\n%s' % (path, redirect_url, max_file_size, max_file_count, expires)
    signature = hmac.new(bytearray(key.encode('utf-8')), hmac_body.encode('utf-8'), hashlib.sha1).hexdigest()

    user = Profile.objects.get(user=request.user)

    context = {
        'swift_url': swift_url, 'redirect_url': redirect_url,
        'max_file_size': max_file_size, 'max_file_count': max_file_count,
        'expires': expires, 'signature': signature, 'user_roles': user.roles.all(),
        'username': user.user.username, 'roles': user.roles.all()
    }

    return render(request, 'index.html', context)

# Create your views here.
roles = Role.objects.all()


def notifications_via_email(container, username, user_email, url):
    mail_subject = "Nuevo archivo en '" + container + "'"
    message = render_to_string('download_email.html', {
        'username': username,
        'container': container,
        'url': url
    })
    from_email = 'coolmensoftware@gmail.com'
    email = EmailMultiAlternatives(mail_subject, message, from_email, to=[user_email])
    email.content_subtype = 'html'

    email.send()

    return 0


def notifications_download(pk):
    so = StorageObject.objects.get(pk=pk)

    storage_url, key, auth_token = get_tempurl_key(so.container)
    storage_url = storage_url.replace("swiftstack", "localhost")
    url = "%s/%s/%s" % (storage_url, so.container, so.objectname)

    expires = int(time.time() + 60)
    path = urlparse(url).path

    hmac_body = 'GET\n%s\n%s' % (expires, path)
    signature = hmac.new(bytearray(key.encode('utf-8')), hmac_body.encode('utf-8'), hashlib.sha1).hexdigest()
    signed_url = '%s?temp_url_sig=%s&temp_url_expires=%s' % (url, signature, expires)

    return str(signed_url)


def tika(request):
    if request.method == 'GET':
        
        # Receive tika data on XHTML format
        # response_data = parser.from_file('/home/frias/sample.pdf', xmlContent=True)
        # Receive tika data on plain text format
        response_data = parser.from_file('credentials.json', settings.TIKA_URL)

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


def get_tempurl_key(container):
    (storage_url, auth_token) = client.get_auth(
        settings.SWIFT_AUTH_URL, settings.SWIFT_USER, settings.SWIFT_PASSWORD)

    try:
        meta = client.head_container(storage_url, auth_token,
                                     container)
        key = meta.get('x-container-meta-temp-url-key')
    except client.ClientException:
        client.put_container(storage_url, auth_token, container)
        key = None

    if not key:
        key = random_key()
        headers = {'x-container-meta-temp-url-key': key}
        client.post_container(storage_url, auth_token,
                              container, headers)

    return storage_url, key, auth_token


def signature(request):
    if request.method == 'POST':
        swift_url = request.POST.get('swift_url')
        #print(swift_url)
        redirect_url = request.POST.get('redirect_url')
        #print(redirect_url)
        max_file_size = request.POST.get('max_file_size')
        #print(max_file_size)
        max_file_count = request.POST.get('max_file_count')
        #print(max_file_count)
        expires = request.POST.get('expires')
        #print(expires)
        container = request.POST.get('container')
        path = urlparse(swift_url).path
        storage_url, key, auth_token = get_tempurl_key(container)
        #print(key)

        hmac_body = '%s\n%s\n%s\n%s\n%s' % (path, redirect_url, max_file_size, max_file_count, expires)
        signature = hmac.new(bytearray(key.encode('utf-8')), hmac_body.encode('utf-8'), hashlib.sha1).hexdigest()
        
        return HttpResponse(
            json.dumps(signature),
            content_type="application/json"
        )


def download(request, pk):
    so = StorageObject.objects.get(pk=pk)

    storage_url, key, auth_token = get_tempurl_key(so.container)
    storage_url = storage_url.replace("swiftstack", "localhost")
    url = "%s/%s/%s" % (storage_url, so.container, so.objectname)

    expires = int(time.time() + 60*60*24*365)
    path = urlparse(url).path

    hmac_body = 'GET\n%s\n%s' % (expires, path)
    signature = hmac.new(bytearray(key.encode('utf-8')), hmac_body.encode('utf-8'), hashlib.sha1).hexdigest()
    signed_url = '%s?temp_url_sig=%s&temp_url_expires=%s' % (url, signature, expires)

    return redirect(signed_url)


def upload(request):
    user = Profile.objects.get(user=request.user)
    roles = Role.objects.all()

    rol = request.GET.get('rol')

    storage_url, key, auth_token = get_tempurl_key(settings.SWIFT_CONTAINER)
    storage_url = storage_url.replace("swiftstack", "localhost")
    prefix = str(uuid.uuid4())

    # Creating dinamically containers according to Django roles
    (container_url, container_token) = client.get_auth(settings.SWIFT_AUTH_URL, settings.SWIFT_USER, settings.SWIFT_PASSWORD)

    headers = {'X-Container-Meta-Access-Control-Allow-Origin': '*', 'x-container-meta-temp-url-key': key}

    for role in roles:
        client.put_container(container_url, container_token, str(role))
        client.post_container(container_url, container_token, str(role), headers)

    # In a real-world scenario you might want to record the prefix in a DB
    # before displaying the form to keep track of user uploads in case the
    # finalize() view is not called. Otherwise there will be data on Swift that
    # is not referenced within your application.
    # For example, run a periodic job that iterates over unused prefixes and
    # check Swift if there are unreferenced uploads

    max_file_size = 5*1024*1024*1024
    max_file_count = 1
    expires = int(time.time() + 60*60*24*365)
    swift_url = "%s/%s/%s/" % (storage_url, settings.SWIFT_CONTAINER, prefix)
    redirect_url = "http://%s%s" % (request.get_host(), reverse(finalize, kwargs={'prefix': prefix, 'container': settings.SWIFT_CONTAINER}))
    path = urlparse(swift_url).path

    hmac_body = '%s\n%s\n%s\n%s\n%s' % (path, redirect_url, max_file_size, max_file_count, expires)
    signature = hmac.new(bytearray(key.encode('utf-8')), hmac_body.encode('utf-8'), hashlib.sha1).hexdigest()

    user = Profile.objects.get(user=request.user)

    context = {
        'swift_url': swift_url, 'redirect_url': redirect_url,
        'max_file_size': max_file_size, 'max_file_count': max_file_count,
        'expires': expires, 'signature': signature, 'user_roles': user.roles.all(),
        'username': user.user.username, 'roles': user.roles.all()
    }

    return render(request, 'upload.html', context)
    

def finalize(request, prefix, container):
    (storage_url, auth_token) = client.get_auth(settings.SWIFT_AUTH_URL, settings.SWIFT_USER, settings.SWIFT_PASSWORD)

    # Note: uploaded objects might not be listed yet due to the eventual
    # consistency. You might want to run an async job after some time to find
    # objects that are already uploaded, but not yet referenced in the DB.
    _meta, objects = client.get_container(storage_url, auth_token, container=container, prefix=prefix)

    # Remember DB ids. These are guessable, thus a real world app should use a
    # more sophisticated approach
    ids = []
    for obj in objects:
        dbentry, _created = StorageObject.objects.get_or_create(
            container=container,
            objectname=obj.get('name'),
            prefix=prefix)
        dbentry.save()
        ids.append(dbentry.id)

    for role in roles:
        if str(role) == str(container):
            role_id = role.id

    for user in Profile.objects.filter(roles=role_id):
        if user.user.username != 'admin':
            for id in ids:
                url = notifications_download(id)
                url = url.replace(" ", "%20")

            # This is needed due to Gmail blocking our mail "spam" hehe
            time.sleep(1)
            notifications_via_email(container, user.user.username, user.user.email, url)


    return render(request, 'finalize.html', {'ids': ids, 'host': request.get_host()})
