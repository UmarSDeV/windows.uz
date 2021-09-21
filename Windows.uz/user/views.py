from django import contrib
from django.contrib.auth.models import User
from user.models import UserProfile
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect, request


from home.models import ContactForm, FAQ
from download.models import Download
from programms.models import Category, Comment
from user.forms import SignUpForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.

@login_required(login_url='/login') # login bo'lganini tekshirish
def index(request):
    currnet_user = request.user
    category = Category.objects.all()
    profile = UserProfile.objects.get(user_id=currnet_user.id)
    context = {
        'category': category,
        'profile':profile
    }
    return render(request, 'userprofile.html', context)

def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            userprofile = UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage'] = userprofile.image.url            
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Login Error!!! Username or Password in incorrect.")
            return HttpResponseRedirect('/login')
    return render(request, 'login_form.html')

def logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def signup_form(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data('username')
            password = form.cleaned_data('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            current_user =request.user
            data = UserProfile
            data.user_id = current_user.id
            data.image = 'image/users/user.png'
            data.save()
            messages.success(request, 'Siz uchun akkount muvaffaqiyatli yaratildi!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/signup')
    form = SignUpForm()
    context = {'form':form}
    return render(request, 'signup_from.html', context)

@login_required(login_url='/login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Sizning akkountingiz muvaffaqiyatli yangilandi')
            return HttpResponseRedirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category':category,
            'user_form':user_form,
            'profile_form':profile_form
        }
        return render(request, 'user_update.html', context)


@login_required(login_url='/login')
def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Sizning parolingiz muvaffaqiyatli yangilandi')
            return HttpResponseRedirect('/user')
        else:
            messages.warning(request, "Iltimos, quyidagi xatolikni to'girlang<br>"+str(form.errors))
            return HttpResponseRedirect('user/password')
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'user_password.html',{'form':form})

@login_required(login_url='/login')
def user_donwloads(request):
    current_user = request.user
    donwloads = Download.objects.filter(user_id = current_user.id)
    context = {
        'downloads':donwloads
    }
    return render(request, 'user_downloads.html', context)


@login_required(login_url='/login')
def user_downloaddetail(request):
    current_user = request.user
    downloads = Download.objects.filter(user_id=current_user.id, id=id)
    downloaditems = Download.objects.filter(download_id=id)
    context = {
        'downloads':downloads,
        'downloaditems':downloaditems,
    }
    return render(request, 'user_downloaddetail.html', context)


@login_required(login_url='/login')
def user_comments(request):
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        'comments':comments,
    }
    return render(request, 'user_comments.html', context)


@login_required(login_url='/login')
def user_deletecomment(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, "Izoh o'chirildi ...")
    return HttpResponseRedirect('/user/comments')

def faq(request):
    category = Category.objects.all()
    faq = FAQ.objects.all(status="True").order_by('ordernumber')
    context = {
        'category':category,
        'faq':faq
    }
    return render(request, 'faq.html', context)
