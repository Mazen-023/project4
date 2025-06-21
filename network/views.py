import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


from .models import User, Post


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


# CRUD
@csrf_exempt
@login_required
def create(request):
    
    # Create a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # Check post content
    data = json.loads(request.body)
    
    # Create post
    post = Post(
        user=request.user,
        content=data.get("content", ""),
    )
    post.save()

    return JsonResponse({"message": "Post created successfully."}, status=201)


@login_required
def read(request):
    posts = Post.objects.all()
    return JsonResponse([post.serialize() for post in posts], safe=False)


@csrf_exempt
@login_required
def update(request, post_id):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

   # Query for requested post
    try:
        post = Post.objects.get(user=request.user, pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)
    
    data = json.loads(request.body)
    post.content = data["content"]
    post.save()
    return HttpResponse(status=204)



@csrf_exempt
@login_required
def delete(request):
    pass


@csrf_exempt
@login_required
def like(request, post_id):

    # Toggle like via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)  
      
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Toggle like
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        return JsonResponse({"likes": post.likes.count()}, status=200)
    else:
        post.likes.add(request.user)
        return JsonResponse({"likes": post.likes.count()}, status=200)
