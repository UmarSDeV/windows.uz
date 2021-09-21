from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from programms.models import *
from .models import *
from user.models import UserProfile
# Create your views here.

def download(request):
    category = Category.objects.all()
    current_user = request.user
    down = Download.objects.filter(user_id=current_user.id)
    context = {
        'category':category,
        'download':down
    }
    return HttpResponseRedirect(request, '/', context)


def download_list(request, id):
    category = Category.objects.all()
    current_user = request.user
    down = Download.objects.filter(down_id=id)
    profile = UserProfile.objects.get(user_id=current_user.id)
    context  = {
        'download':down,
        'category':category,
        'profile':profile
    }
    return render(request, 'download_list.html', context)


@login_required(login_url='/login')
def deletefrom_download(request, id):
    Download.objects.filter(id=id).delete()
    messages.success(request, "Dastur yuklab olinganlar ro'yxatidan o'chirildi!")
    return HttpResponseRedirect('/download')
