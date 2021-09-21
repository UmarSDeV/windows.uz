from django import forms
from django.shortcuts import render
from django.core.checks import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from programms.models import *
from favourites.models import *
from user.models import UserProfile
from .models import Favourite, FavouriteForm
# Create your views here.

@login_required(login_url='/login')
def addto_favourite(request):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    programm = Programm.objects.get(pk=id)
    checkin_favourite = Favourite.objects.filter(programm_id=id, user_id=current_user.id)
    if checkin_favourite:
        control = 1
    else:
        control = 0
    if request.method == 'POST':
        form = FavouriteForm(request.POST)
        if form.is_valid():
            if control == 1:
                data = Favourite.objects.filter(product_id=id, user_id=current_user.id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else:
                data = Favourite()
                data.user_id = current_user.id
                data.programm_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, 'Programm added to Favourites')
        return HttpResponseRedirect(url)
    else:
        if control == 1:
            data = Favourite.objects.get(programm_id=id, user_id=current_user.id)
            data.quantity += 1
            data.save()

        else:
            data = Favourite()
            data.user_id = current_user.id
            data.programm_id = id
            data.save()
        messages.success(request, 'Programm added to Favourites')
        return HttpResponseRedirect(url)

@login_required(login_url='/login')
def deletefrom_favourites(requset, id):
    Favourite.objects.filter(id=id).delete()
    messages.success(requset, 'Your programm deleted from Favourites')
    return HttpResponseRedirect('/favourites')