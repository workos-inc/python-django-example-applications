import os
import json
from django.http.response import HttpResponse
import workos
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

workos.api_key = os.getenv('WORKOS_API_KEY')
workos.base_api_url = 'http://localhost:8000/' if settings.DEBUG else workos.base_api_url
directory_id = os.getenv('DIRECTORY_ID')  # Follow the WorkOS guide to get this

def get_home(request):
    print('request', request)
    directories = workos.client.directory_sync.list_directories()
    directories = directories['data']
    return render(request, 'directory_sync/home.html', {"directories": directories})

def get_directory(request):
    directory_id = request.GET['id']
    directory = workos.client.directory_sync.get_directory(directory_id)
    return render(request, 'directory_sync/directory.html', {"directory_id": directory_id, "directory": directory})

def get_directory_users(request):
    directory_id = request.GET['id']
    users = workos.client.directory_sync.list_users(directory=directory_id)
    return render(request, 'directory_sync/users.html', {"users": users})


def get_directory_groups(request):
    directory_id = request.GET['id']
    groups = workos.client.directory_sync.list_groups(directory=directory_id)
    return render(request, 'directory_sync/groups.html', {"groups": groups})

@csrf_exempt
def webhooks(request):
    dict_payload = json.loads(request.body)
    payload = json.dumps(dict_payload)
    sig_header = request.headers.get('WorkOS-Signature')

    response = workos.client.webhooks.verify_event(
        payload = payload,
        sig_header = sig_header,
        secret = os.getenv('WEBHOOKS_SECRET')
    )

    print(response)

    return HttpResponse(200)
