from django.conf.urls import url
from .views import (PostCreate,
                    PostDelete,
                    PostList,
                    comment_to_post,
                    CommentDelete,
                    )

app_name = "app"

urlpatterns = [
    url(r'^create/$', PostCreate.as_view(), name="create"),
    url(r'^delete/(?P<pk>\d+)/$', PostDelete.as_view(), name="delete"),
    url(r'^comment/(?P<pk>\d+)/$', comment_to_post, name="comment"),
    url(r'^comment/delete/(?P<pk>\d+)/$', CommentDelete.as_view(), name="comment_delete"),
    url(r'^$', PostList.as_view(), name="list"),
]
