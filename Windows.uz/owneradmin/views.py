from django.contrib.auth.models import User
from programms.froms import CreateCategoryForm, CreateProgrammForm, EditProgrammForm
from programms.models import Category, Comment, Programm
from download.models import Download

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate

# Create your views here.
def admin_login(request):
    if not request.user.is_authenticated & request.user.is_superuser:
        return render('admin_home.html')
    elif request.method == "POST":
        username = request.POST['admin']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        context = {
            'programm': Programm,
            'category': Category
            }
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'admin_home.html', context)
            else:
                return render(request, 'admin_login.html',
                              {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'admin_login.html', {'error_message': 'Invalid login'})
    return render(request, 'admin_login.html')

def create_category(request):
    if not request.user.is_authenticated & request.user_is_superuser:
        return render('admin_home.html')
    else:
        form = CreateCategoryForm(request.POST or None)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect('category_admin')
        return render(request, 'create_category.html', {'form':form})

def create_programm(request):
    if not request.user.is_authenticated & request.user.is_superuser:
        return render('admin_home.html')
    else:
        form = CreateProgrammForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            programm = form.save(commit=False)
            if request.FILES:
                programm.programm_image = request.POST['programm_image']
                programm.programm_torrent = request.POST['programm_torrent']
            programm.save()
            return redirect('programms_admin')
    return render(request, 'create_programm.html', {'form':form})

def programm_edit(request):
    if not request.user.is_authenticated & request.user.is_superuser:
        return render(request, 'admin_login.html')
    else:
        programm = get_object_or_404(Programm, id=1)
        context = {
            'title': programm.title,
            'keywords': programm.keywords,
            'description': programm.description,
            'detail': programm.detail,
            'torrent':programm.torrent,
            'image':programm.image,
            'link':programm.link
        }
        form = EditProgrammForm(request.POST or None, request.FILES or None, initial=context),
        if form.is_valid():
            programm.title = form.cleaned_data['title']
    return render(request, 'programm_edit', context)


def user_edit(request):
    if not request.user.is_authenticated & request.user.is_superuser:
        return render(request, 'admin_login.html')
    else:
        user = get_object_or_404(User, id=1)
        context = {
            'user_first_name':user.first_name,
            'user_email':user.email,
            'user_phone':user.phone,
        }
        user_comments = Comment.objects.filter(user_id=id)
        user_downloads = Download.objects.filter(down_id=id)
    return render(request,'user_edit.html',context)
    
def logout_admin(request):
    logout(request)
    return render(request, 'admin_login.html')