from django.http import HttpResponse

def index(request, username):
    return HttpResponse(f"Hello '{username}'!")