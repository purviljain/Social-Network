from django.conf.urls import url
from .views import (PostCreate,PostDelete,PostList,comment_to_post,CommentDelete,like,)
app_name = "app"
urlpatterns = [
    url(r'^create/$', PostCreate, name="create"),
    url(r'^delete/(?P<pk>\d+)/$', PostDelete, name="delete"),
    url(r'^comment/(?P<pk>\d+)/$', comment_to_post, name="comment"),
    url(r'^like/(?P<pk>\d+)/$', like, name="like"),
    url(r'^comment/delete/(?P<pk>\d+)/$', CommentDelete, name="comment_delete"),
    url(r'^$', PostList, name="list"),
]
