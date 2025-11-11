from django.shortcuts import render


def client1(request):
    """Render client 1 chat page"""
    return render(request, 'client1.html')


def client2(request):
    """Render client 2 chat page"""
    return render(request, 'client2.html')


def index(request):
    """Render index page"""
    return render(request, 'index.html')
