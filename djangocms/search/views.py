from django.shortcuts import render
from users.models import Role, Profile

# Create your views here.

def search(request):
    user = Profile.objects.get(user=request.user)
    roles = Role.objects.all()

    context = {
        'roles': user.roles.all()
    }

    return render(request, 'search.html', context)
