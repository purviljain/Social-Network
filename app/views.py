from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import Post, Comment, Like, Follower
from .forms import PostForm, CommentForm
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
# Create your views here.

def PostList(request):
    post=Post.objects.all()
    app = []
    for p in post:
        if Follower.objects.filter(user=p.user):
            temp = Follower.objects.get(user=p.user)
            if temp:
                qs = temp.followers.all()
                print(qs)
                for i in qs:
                    if i == request.user:
                        app.append(p)
        if p.user == request.user:
            app.append(p)
    return render(request,'app/index.html',{'follow':temp,'app':app})

def Users(request):
    all_users = User.objects.all()
    return render(request, 'app/users.html', {'all_users':all_users})

def UserProfile(request,pk):
    user = User.objects.get(pk=pk)
    print (pk)
    print (user)
    if(user.is_active):
        post = Post.objects.filter(user=user)
        print(post)
        temp = Follower.objects.all()
        return render(request, 'app/userprofile.html', {'follow':temp,'user':user,'post':post})

@login_required(login_url='login')
def PostCreate(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
        post=Post.objects.all()
        app = []
        for p in post:
            if Follower.objects.filter(user=p.user):
                temp = Follower.objects.get(user=p.user)
                if temp:
                    qs = temp.followers.all()
                    print(qs)
                    for i in qs:
                        if i == request.user:
                            app.append(p)
            if p.user == request.user:
                app.append(p)
        return render(request,'app/index.html',{'follow':temp,'app':app})
    else:
        app = Post.objects.all()
        form = PostForm()
    return render(request, 'app/create.html', {'form': form, 'app':app})

@login_required(login_url='login')
def PostDelete(request,pk):
    try:
        post = Post.objects.get(id=pk)
        if request.user == post.user:
            post.delete()
            post=Post.objects.all()
            app = []
            for p in post:
                if Follower.objects.filter(user=p.user):
                    temp = Follower.objects.get(user=p.user)
                    if temp:
                        qs = temp.followers.all()
                        print(qs)
                        for i in qs:
                            if i == request.user:
                                app.append(p)
                if p.user == request.user:
                    app.append(p)
            return render(request,'app/index.html',{'follow':temp,'app':app})
        else:
            return render(request, 'app/not_allowed.html', {"txt": "You are not allowed to delete this."})
    except Exception as e:
        print (e)
        return render(request, 'app/not_allowed.html', {"txt": "No such post exists."})

@login_required(login_url='login')
def comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user_id = request.user.id
            comment.post = post
            comment.save()
        return redirect('/app/')
    else:
        form = CommentForm()
    return render(request, 'app/comment_create.html', {'form': form})

@login_required(login_url='forum:login')
def CommentDelete(request,pk):
    try:
        comment = Comment.objects.get(id=pk)
        if request.user == comment.user:
            comment.delete()
            post=Post.objects.all()
            app = []
            for p in post:
                if Follower.objects.filter(user=p.user):
                    temp = Follower.objects.get(user=p.user)
                    if temp:
                        qs = temp.followers.all()
                        print(qs)
                        for i in qs:
                            if i == request.user:
                                app.append(p)
                if p.user == request.user:
                    app.append(p)
            return render(request,'app/index.html',{'follow':temp,'app':app})
        else:
            return render(request, 'app/not_allowed.html', {"txt": "You are not allowed to delete this."})
    except Exception as e:
        print (e)
        return render(request, 'app/not_allowed.html', {"txt": "No such comment exists."})

@login_required(login_url='forum:login')
def like(request, pk):
    post = Post.objects.get(id=pk)
    user = request.user
    like = Like.objects.filter(user=user, post=post)
    if like.exists():
        # like.delete()
        post=Post.objects.all()
        app = []
        for p in post:
            if Follower.objects.filter(user=p.user):
                temp = Follower.objects.get(user=p.user)
                if temp:
                    qs = temp.followers.all()
                    print(qs)
                    for i in qs:
                        if i == request.user:
                            app.append(p)
            if p.user == request.user:
                app.append(p)
        return render(request,'app/index.html',{'follow':temp,'app':app})
    like = Like.objects.create(user=user, post=post)
    like.save()
    like = Like.objects.get(user=user, post=post)
    post=Post.objects.all()
    app = []
    for p in post:
        if Follower.objects.filter(user=p.user):
            temp = Follower.objects.get(user=p.user)
            if temp:
                qs = temp.followers.all()
                print(qs)
                for i in qs:
                    if i == request.user:
                        app.append(p)
        if p.user == request.user:
            app.append(p)
    return render(request,'app/index.html',{'follow':temp,'app':app})
    # like = get_object_or_404(Like, pk=pk)
    # app = Post.objects.all()
    # return render(request,'app/index.html',{'app':app})

def Follow_view(request,pk):
    user = User.objects.get(pk=pk)
    follow = Follower.objects.filter(user=user)
    if follow.exists():
        follow = Follower.objects.get(user=user)
        follow.followers.add(request.user)
    else:
        f1 = Follower(user=user)
        f1.save()
        f1.followers.add(request.user)
    f1 = Follower.objects.get(user=user)
    print(f1)
    post = Post.objects.filter(user=user)
    temp = Follower.objects.all()
    return render(request, 'app/userprofile.html', {'follow':temp,'user':user,'post':post})
