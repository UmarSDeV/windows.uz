from django import contrib
from django.shortcuts import render
import json
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, query
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request


from home.models import *
from home.forms import SearchForm
from programms.models import *
from user.models import UserProfile
# Create your views here.

def index(request):
    setting = Setting.objects.filter(pk=1)
    programms_latest = Programm.objects.all().order_by('-id')[:4]
    programms_slider = Programm.objects.all().order_by('id')[:4]
    programms_picked = Programm.objects.all().order_by('?')[:4]
    page = 'home'
    context = {
        'setting':setting,
        'programms_latest':programms_latest,
        'programms_slider':programms_slider,
        'programms_picked':programms_picked
    }
    return render(request, 'index.html', context)

def aboutus(request):
    setting = Setting.objects.get(pk=1)
    return render(request, 'aboutus.html', {'setting':setting})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = form.cleaned_data['REMOTE_ADDR']
            data.save()
            messages.success(request, "Sizning xabaringiz muvaffaqiyatli jo'natildi! Xabar uchun rahmat")
            return HttpResponseRedirect('/contact')
    setting = Setting.objects.filter(pk=1)
    context = {
            'form':form,
            'setting':setting
        }
    return render(request, 'contact.html', context)

def category_products(request):
    catdata = Category.objects.get(pk=id)
    programms = Programm.objects.filter(category_id=id)
    context = {
        'catdata':catdata,
        'programms':programms
    }
    return render(request, 'category_products.html', context)

def search(requset):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            if catid == 0:
                programms = Programm.objects.filter(title_icontains=query)
            else:
                programms = Programm.objects.filter(title__icontains=query, category_id = catid)
            category = Category.objects.all()
            context = {
                'query':query,
                'catid':catid,
                'category':category,
                'programms':programms,
            }
            return render(request, 'search_programm.html', context)
    return HttpResponseRedirect('/')

def searchauto(request):
    if request.is_ajax():
        query = request.GET.get('term', '')
        programms = Programm.objects.filter(title__icontains=query)
        results = []
        for prog in programms:
            programms_json = {}
            programms_json = prog.title + '>' + prog.category.title
            results.append(programms_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    jsontype = 'app/json'
    return HttpResponse(data, jsontype)

def product_detail(request, id, slug):
    query = request.GET.get('q')
    category = Category.objects.all()
    programms = Programm.objects.filter(pk=id)
    images = Images.objects.filter(programm_id=id)
    comments = Comment.objects.filter(status ="True", programm_id=id)
    context = {
        'query':query,
        'category':category,
        'programms':programms,
        'images':images,
        'comments':comments
    }
    return render(request, 'product_detail.html', context)

def faq(request):
    if request.method == "POST":
        faqq = FAQ.objects.filter(status="True", faqq_id=id).order_by("ordernumber")
    return render(request, 'faq.html', {'faqq':faqq})


from django import template
from windows_config import settings

register = template.Library()
@register.simple_tag()
def categorylist():
    return Category.objects.all()

@register.simple_tag()
def categoryTree(id, menu):
    if id<=0:
        query = Category.objects.filter(parent_id__isnull=True).order_by("id")
        querycount = Category.objects.filter(parent_id__isnull=True).count()
    else:
        query = Category.objects.filter(parent_id=id)
        querycount = Category.objects.filter(parent_id=id)
    if querycount >0:
        for q in query:
            sub_category_count = Category.objects.filter(parent_id=q.id).count()
            if sub_category_count>0:
                menu += '\t<li class="dropdown side-dropdown">\n'
                menu += '\t<a class="dropdown-toggle" data-toggle="dropdown" aria-expanded="true">'+q.title+'i class="fa fa-angle-right"></i></a>\n'
                menu += '\t\t<div class="custom-menu">\n'
                menu += '\t\t\t<ul class="list-links">\n'
                menu += categoryTree(int(q.id))
                menu += '\t\t\t</ul>\n'
                menu += '\t\t</div>\n'
                menu += '\t</li>\n\n'
            else:
                menu += '\t\t\t\t<li><a href="'+reverse('category_products', args=(q.id, q.slug))+'">"'+q.title+'</a></li>\n'
    return menu


