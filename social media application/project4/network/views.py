from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Posts, Comments, FFowers
from django.core.serializers import serialize
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import CreatePost, AddComments
from django.core import serializers

from .models import User


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
@login_required
def posts(request, limit, start):
    posts = Posts.objects.exclude(owner=request.user.id).order_by("-timestamp").all()[start:start+limit]

    post_data_list = []

    for post in posts:
        post_data = {
            'model': 'network.posts',
            'pk': post.pk,
            'fields': {
                'owner': post.owner_id,
                'owner_name': post.owner_name,
                'name': post.name,
                'likes': post.likes,
                'picture_link': post.picture_link.url,
                'timestamp': post.timestamp,
                'liked_by': list(post.liked_by.values_list('id', flat=True)),
                'followers': list(FFowers.objects.filter(user=post.owner).values_list('followers__id', flat=True))
            }
        }
        post_data_list.append(post_data)


    response_data = {
        'posts': post_data_list,
        'request_data': {
            'user_id': request.user.id,
            'username': request.user.username,
        }
    }
    
    return JsonResponse(response_data, safe=False)

def following(request, limit, start):
    follows = FFowers.objects.filter(user=request.user)
    following_ids = follows.values_list('following__id', flat=True)

    posts = Posts.objects.filter(owner_id__in=following_ids).order_by("-timestamp")[start:start+limit]

    post_data_list = []
    for post in posts:
        post_data = {
            'model': 'network.posts',
            'pk': post.pk,
            'fields': {
                'owner': post.owner_id,
                'owner_name': post.owner_name,
                'name': post.name,
                'likes': post.likes,
                'picture_link': post.picture_link.url,
                'timestamp': post.timestamp,
                'liked_by': list(post.liked_by.values_list('id', flat=True)),
                'followers': list(FFowers.objects.filter(user=post.owner).values_list('followers__id', flat=True))
            }
        }
        post_data_list.append(post_data)

    response_data = {
        'posts': post_data_list,
        'request_data': {
            'user_id': request.user.id,
            'username': request.user.username,
        }
    }

    return JsonResponse(response_data, safe=False)

def following_page(request):
    return render(request, 'network/following.html')

def create_post(request):
    if request.method == "POST":
        form = CreatePost(request.POST, request.FILES, request=request)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = CreatePost()  

    return render(request, "network/create.html", {
        'form': form
    })


def index(request):
    return render(request, "network/index.html")

def profile(request):
    if request.user.is_authenticated:
        user_posts = Posts.objects.filter(owner=request.user)
        return render(request, "network/profile.html", {
            'posts':user_posts
        })

def delete_post(request, post_id):
    Posts.objects.filter(id=post_id).delete()
    return JsonResponse({'success': True})

def delete_comment(request, comment_id):
    Comments.objects.filter(pk=comment_id).delete()
    return JsonResponse({'success': True})

def like_post(request, post_id):
    post = Posts.objects.get(id=post_id)
    if not post.liked_by.filter(id=request.user.id).exists():
        post.likes += 1
        post.liked_by.add(request.user)
        post.save()
        return JsonResponse({'success': True})
    else:
        post.likes -= 1
        post.liked_by.remove(request.user)
        post.save()
        return JsonResponse({'success': False})
    
def follow(request, post_id):
    post = Posts.objects.get(pk=post_id)
    user = request.user

    try:
        ffowers = FFowers.objects.get(user=user)
    except FFowers.DoesNotExist:
        ffowers = FFowers.objects.create(user=user)

    try:
        post_owner = FFowers.objects.get(user=post.owner)
    except FFowers.DoesNotExist:
        post_owner = FFowers.objects.create(user=post.owner)

    if post.owner not in ffowers.following.all():
        ffowers.following.add(post.owner)
        ffowers.save()
        post_owner.followers.add(user)
        post_owner.save()
        return JsonResponse({'success': True})
    else:
        ffowers.following.remove(post.owner)
        ffowers.save()
        post_owner.followers.remove(user)
        return JsonResponse({'success': False})

def comments(request, post_id):
    comments = Comments.objects.filter(post_id=post_id)
    for comment in comments:
        username = comment.owner.username
        comment.username = username

    if request.method == 'POST':
        form = AddComments(request.POST, request=request, post_id=post_id)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('comments', args=[post_id]))
    else:
        form = AddComments(request=request, post_id=post_id)

    return render(request, 'network/comments.html', {
        'comments': comments,
        'form': form
    })

def edit_post(request, post_id):
    post = Posts.objects.get(pk=post_id)
    form = CreatePost(instance=post)

    if request.method == 'POST':
        form = CreatePost(request.POST, request.FILES, instance=post, request=request)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile'))
    
    return render(request, 'network/edit.html', {'form': form})



def favicon(request):
    return HttpResponse(status=204)

def following_list(request):
    followings = FFowers.objects.filter(user=request.user)
    following_users = [follow.following.all() for follow in followings]
    return render(request, 'network/following_list.html', {
        'following': following_users
    })


def followers_list(request):
    followers = FFowers.objects.filter(user=request.user)
    followers_users = [follow.followers.all() for follow in followers]
    return render(request, 'network/followers_list.html', {
        'followers': followers_users
    })

def other_profile(request, user_id):
    posts = Posts.objects.filter(owner=user_id)
    post_data_list = []

    for post in posts:
        post_data = {
            'model': 'network.posts',
            'pk': post.pk,
            'fields': {
                'owner': post.owner_id,
                'owner_name': post.owner_name,
                'name': post.name,
                'likes': post.likes,
                'picture_link': post.picture_link.url,
                'timestamp': post.timestamp,
                'liked_by': list(post.liked_by.values_list('id', flat=True)),
                'followers': list(FFowers.objects.filter(user=post.owner).values_list('followers__id', flat=True))
            }
        }
        post_data_list.append(post_data)


    response_data = {
        'posts': post_data_list,
        'request_data': {
            'user_id': request.user.id,
            'username': request.user.username,
        }
    }
    
    return JsonResponse(response_data, safe=False)

def other_profile_page(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, 'network/other.html', {
        'user': user
    })