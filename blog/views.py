from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Post
from django.utils import timezone
from .forms import PostForm


# Create your views here.

def home(request):
    posts = Post.objects.all()  # Post.objects.filter(user=request.user) Login User Data
    return render(request, 'blog/home.html', {'posts': posts})


def signup(request):
    if request.method == 'GET':
        return render(request, 'auth/signup.html', )  # {'form': UserCreationForm()}
    else:
        if request.POST['password0'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['peoplename'],
                                                password=request.POST['password0'])
                user.save()
                login(request, user)
                return redirect('blog')
            except IntegrityError:
                return render(request, 'auth/signup.html', {'name_error': 'UserName Already Taken'})
        else:
            return render(request, 'auth/signup.html', {'pass_error': 'password not match'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'auth/login.html')
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'auth/login.html', {'error': 'Username Or Password Did Not Match'})
        else:
            login(request, user)
            return redirect('blog')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('blog')


@login_required(login_url="loginuser")
def create(request):
    if request.method == 'GET':
        return render(request, 'blog/create.html')
    else:
        try:
            form = PostForm(request.POST)
            newpost = form.save(commit=False)
            newpost.user = request.user
            newpost.save()
            return redirect('blog')
        except ValueError:
            return render(request, 'blog/create.html', {'error': 'Enter Correct Data'})


@login_required(login_url="loginuser")
def myfeed(request):
    posts = Post.objects.filter(user=request.user)
    return render(request, 'blog/myfeed.html', {'posts': posts})


@login_required(login_url='loginuser')
def editfeed(request, feed_pk):
    upost = get_object_or_404(Post, pk=feed_pk, user=request.user)

    if request.method == 'GET':
        form = PostForm(instance=upost)
        return render(request, 'blog/editfeed.html', {'upost': upost})
    else:
        try:
            form = PostForm(request.POST, instance=upost)
            form.save()
            return redirect('myfeed')
        except ValueError:
            return render(request, 'blog/editfeed.html', {'upost': upost, 'error': 'BAD Data'})


@login_required(login_url='loginuser')
def deletefeed(request, feed_pk):
    upost = get_object_or_404(Post, pk=feed_pk, user=request.user)

    if request.method == 'POST':
        upost.delete()
        return redirect('myfeed')
