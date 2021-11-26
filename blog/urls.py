from django.urls import path

from . import views

urlpatterns = [
    # path("", views.starting_page, name="starting-page"),
    path("", views.StartingPage.as_view(), name="starting-page"),
    # path("posts", views.posts, name="posts-page"),
    path("posts", views.AllPosts.as_view(), name="posts-page"),
    # path("posts/<slug:slug>", views.post_detail, name="post-detail-page")  # /posts/my-first-post
    path("posts/<slug:slug>", views.PostDetail.as_view(), name="post-detail-page"),  # /posts/my-first-post
    path("read-later", views.ReadLaterView.as_view(), name="read-later")
]
