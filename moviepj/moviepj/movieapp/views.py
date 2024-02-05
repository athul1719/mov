# from django.http import HttpResponse
# from django.shortcuts import render, redirect
# from .models import Movie
# from django.contrib.auth.models import User
# from django.core.checks import messages
# from django.shortcuts import render, redirect
# from django.contrib import messages,auth
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.contrib.sitemaps.views import index
from django.core import paginator
from django.core.checks import messages
from django.core.paginator import EmptyPage, InvalidPage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from django.core.paginator import Paginator,EmptyPage,InvalidPage

from movieapp.forms import MovieForm

from .models import Movie, Category


# Create your views here.
def home(request):
    movie=Movie.objects.order_by('-id')
    request_user = request.user
    return render(request, 'home.html', {"movielist": movie,"request_user": request_user})

def profile(request):
    return render(request,'profile.html')
# def register(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         email = request.POST['email']
#         password = request.POST['password']
#         cpassword = request.POST['password1']
#         if password == cpassword:
#             if User.objects.filter(username=username).exists():
#                 messages.info(request, "username taken")
#                 return redirect('register')
#         elif User.objects.filter(email=email).exists():
#             messages.info(request, "email taken")
#             return redirect('register')
#         else:
#             user = PetOwner(username=username, first_name=first_name, last_name=last_name, email=email,
#                                             password=password)
#             user.save();
#             return redirect('login')
#     else:
#         messages.info(request, "password not match")
#         return redirect(reverse('movieapp:register'))
#     return redirect('/')
#     return render(request, 'register.html')

def register(request):
    if request.method=='POST':
        username=request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']
        cpassword = request.POST['password1']
        if password==cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request,"username taken")
                return redirect(reverse('movieapp:register'))
            elif User.objects.filter(email=email).exists():
                messages.info(request,"email taken")
                return redirect(reverse('movieapp:register'))
            else:
                user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
                user.save();
                return redirect(reverse('movieapp:login'))

        else:
            messages.info(request, "password not match")
            return redirect(reverse('movieapp:register'))
        return redirect('/')
    return render(request,'register.html')

def add(request, obj=None):
    cat = Category.objects.all()
    if request.method=='POST':
        name=request.POST.get('name')
        desc = request.POST.get('desc')
        date = request.POST.get('date')
        actors = request.POST.get('actors')
        category = request.POST.get('category')
        trailer = request.POST.get('trailer')
        img = request.FILES['img']
        owner = request.user
        category_obj = Category.objects.get(name=category)
        ins = Movie(name=name,desc=desc,date=date,actors=actors,category=category_obj,trailer=trailer,img=img,owner=owner)
        ins.save()
    categories = Category.objects.filter()

    return render(request, "add.html", {"category": categories})


def detail(request,movie_id):
    movie=Movie.objects.get(id=movie_id)
    return render(request,'detail.html',{'movie':movie})



def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password = request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/' )
        else:
            messages.info(request, "invalid  credential")
            return redirect(reverse('movieapp:login'))
    return render(request,'login.html')



def update(request,id):
    movie=Movie.objects.get(id=id)
    form=MovieForm(request.POST or None, request.FILES,instance=movie)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request,'edit.html',{'form':form,'movie':movie})

def delete(request,id):
    if request.method=='POST':
        movie=Movie.objects.get(id=id)
        movie.delete()
        return redirect('/')
    return render(request,'delete.html')


def search(request):
    movie=None
    query=None
    if 'q' in request.GET:
        query=request.GET.get('q')
        movie=Movie.objects.all().filter(Q(name__contains=query) | Q(desc__contains=query))
    return  render(request,'search.html', {'query':query,'movie':movie})


# def moviecat(request,c_slug=None):
#     c_page=None
#     movies=None
#     if c_slug!=None:
#         c_page=get_object_or_404(Category,slug=c_slug)
#         movies=Movie.objects.all().filter(category=c_page,available=True)
#     else:
#         movies=Movie.objects.all().filter(available=True)
#     return  render(request,"category.html",{'category':c_page,'movies':movies})
#
#

def moviecat(request,c_slug=None,published=True):
    c_page=None
    products_list=None
    if c_slug!=None:
        c_page=get_object_or_404(Category,slug=c_slug)
        products_list=Movie.objects.all().filter(category=c_page)
    else:
        products_list=Movie.objects.all().filter()
    paginator=Paginator(products_list,6)
    try:
        page=int(request.GET.get('page','1'))
    except:
        page=1
    try:
        movie=paginator.page(page)
    except (EmptyPage,InvalidPage):
        movie=paginator.page(paginator.num_pages)
    return  render(request,"category.html",{'category':c_page,'movie':movie})



def movdetail(request, c_slug,movies_slug):
    try:
        movies=Movie.objects.get(category__slug=c_slug,slug=movies_slug)
    except Exception as e:
        raise e
    return render(request,'detail.html',{'movie':movies})



def just_registered(request):
    just_registered = False
    if request.user.is_authenticated() and request.user.email:
        if request.user.date_joined < datetime.today() + timedelta(minutes=2):
            if 'just_registered' not in request.session:
                just_registered = True
                request.session['just_registered'] = just_registered
    return { 'just_registered' : just_registered }


def logout(request):
    auth.logout(request)
    return  redirect('/')
