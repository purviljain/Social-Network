from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import Post, Comment, Like
from .forms import PostForm, CommentForm
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import FormUserNeededMixin, UserOwnerMixin
from django.contrib.auth.decorators import login_required
# Create your views here.


class PostList(ListView):
    template_name = 'app/index.html'
    context_object_name = 'app'

    def get_queryset(self):
        return Post.objects.all()

@login_required(login_url='login')
def PostCreate(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
        app = Post.objects.all()
        return render(request,'app/index.html',{'app':app})
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
            app = Post.objects.all()
            return render(request,'app/index.html',{"app":app})
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
            app = Post.objects.all()
            return render(request,'app/index.html',{"app":app})
        else:
            return render(request, 'app/not_allowed.html', {"txt": "You are not allowed to delete this."})
    except Exception as e:
        print (e)
        return render(request, 'app/not_allowed.html', {"txt": "No such comment exists."})
    # model = Comment
    # template_name = "app/comm_delete.html"
    # success_url = reverse_lazy("app:list")
    # def delete(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     if self.object.user == request.user:
    #         self.object.delete()
    #         return HttpResponseRedirect(self.get_success_url())
    #     else:
    #         return render(request, 'app/not_allowed.html', {"txt": "You are not allowed to delete this."})

@login_required(login_url='forum:login')
def like(request, pk):
    if request.method == 'POST':
        post = Post.objects.get(id=pk)
        user = request.user
        like = Like.objects.filter(user=user, post=post)
        if like.exists():
            # like.delete()
            app = Post.objects.all()
            return render(request,'app/index.html', {"pk":pk,'app':app,"like":like})
        like = Like.objects.create(user=user, post=post)
        like.save()
        like = Like.objects.get(user=user, post=post)
        app = Post.objects.all()
        return render(request,'app/index.html', {"pk":pk,'app':app,"like":like})
        # else:
        #     return redirect('forum:login')
    like = get_object_or_404(Like, pk=pk)
    app = Post.objects.all()
    return render(request,'app/index.html',{'app':app})
