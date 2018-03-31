from django.contrib import admin
from django.conf.urls import url,include
from signup.views import login_view, logout_view, register, profile
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^booklisting/', include('book_listing.urls', namespace="books")),
    # url(r'^sign_in/', include('sign_in.urls', namespace="sign_in")),
    # url(r'^signup/', include('signup.urls', namespace="signup")),
    url(r'^register/', register, name="register"),
    url(r'^profile/', profile, name="profile"),
    url(r'^app/', include('app.urls', namespace="app")),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^$', views.home, name='home'),
    # url(r'^forum/', include('forum.urls', namespace="forum")),
]
