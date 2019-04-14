from django.shortcuts import render, redirect
from Locus.asgi import channel_layer
from asgiref.sync import async_to_sync

from .models import UrlForm


def search(request):
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            return run_components(form.cleaned_data['duration'])
    else:
        form = UrlForm()
    return render(request, 'search.html', {'form': form})


def run_components(duration):
    dur = int(duration) / 3

    print("Sending messages to components")

    async_to_sync(channel_layer.send)('crawler', {'type': "process", 'duration': dur})
    async_to_sync(channel_layer.send)('some_component', {'type': "process", 'duration': dur})
    async_to_sync(channel_layer.send)('another_component', {'type': "process", 'duration': dur})
    print("Sent")

    return redirect('/result/')


def result(request):
    return render(request, 'result.html')

