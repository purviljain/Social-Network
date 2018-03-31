from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import FormUserNeededMixin, UserOwnerMixin
# Create your views here.


class PostList(ListView):
    template_name = 'app/index.html'
    context_object_name = 'app'

    def get_queryset(self):
        return Post.objects.all()


class PostCreate(LoginRequiredMixin, FormUserNeededMixin, CreateView):
    template_name = "app/create.html"
    form_class = PostForm
    model = Post
    login_url = "/admin/"
    success_url = reverse_lazy("app:list")
    context_object_name = 'app'


class PostDelete(LoginRequiredMixin, UserOwnerMixin, DeleteView):
    model = Post
    template_name = "app/delete.html"
    success_url = reverse_lazy("app:list")
    context_object_name = 'app'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == request.user:
            self.object.delete()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return render(request, 'app/not_allowed.html', {"txt": "You are not allowed to delete this."})


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


class CommentDelete(LoginRequiredMixin, UserOwnerMixin, DeleteView):
    model = Comment
    template_name = "app/comm_delete.html"
    success_url = reverse_lazy("app:list")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == request.user:
            self.object.delete()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return render(request, 'app/not_allowed.html', {"txt": "You are not allowed to delete this."})
