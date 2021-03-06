from datetime import date
from typing import List
from .models import Post
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .forms import CommentForm
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse

# def get_date(post):
#   return post['date']


class StartingPage(ListView):
	template_name = "blog/index.html"
	model = Post
	ordering = "-date"
	context_object_name = 'posts'

	def get_queryset(self):
		querySet = super().get_queryset()
		data = querySet[:3]
		return data

# def starting_page(request):
#     all_posts = Post.objects.all().order_by("-date")[:3]
#     all_posts = reversed(all_posts)
#     return render(request, "blog/index.html", {
#       "posts": all_posts
#     })


class AllPosts(ListView):
	template_name = "blog/all-posts.html"
	model = Post
	ordering = ["-date"]
	context_object_name = "all_posts"

# def posts(request):
#     all_posts = Post.objects.all()
#     return render(request, "blog/all-posts.html", {
#       "all_posts": all_posts
#     })

# class PostDetail(DetailView):
#   template_name = "blog/post-detail.html"
#   model = Post
#   context_object_name = "post"
#   def get_context_data(self, **kwargs):
#       context = super().get_context_data(**kwargs)
#       context["post_tags"] = self.object.tags.all()
#       context["comment_form"] = CommentForm()
#       return context


# def post_detail(request, slug):
#     identified_post = Post.objects.get(slug=slug)
#     return render(request, "blog/post-detail.html", {
#       "post": identified_post,
#       "post_tags" : identified_post.tags.all()
#     })


class PostDetail(View):
	def get(self, request, slug):
		post = Post.objects.get(slug=slug)
		context = {
			'post': post,
			"post_tags": post.tags.all(),
			"comment_form": CommentForm(),
			"comments": post.comments.all().order_by("-id")
		}
		return render(request, "blog/post-detail.html", context)

	def post(self, request, slug):
		comment_form = CommentForm(request.POST)
		post = Post.objects.get(slug=slug)
		if comment_form.is_valid():
			comment = comment_form.save(commit=False)
			comment.post = post
			comment.save()
			return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))
		context = {
			'post': post,
			"post_tags": post.tags.all(),
			"comment_form": comment_form,
			"comments": post.comments.all().order_by("-id")
		}
		return render(request, "blog/post-detail.html", context)

class ReadLaterView(View):

	def get(self, request):
		stored_posts = request.session.get("stored_posts")
		context = {}
		if stored_posts is None or len(stored_posts) == 0:
			context["posts"] = []
			context["has_posts"] = False
		else:
			context["posts"] = Post.objects.filter(id__in=stored_posts)
			context["has_posts"] = True
		return render(request, "blog/read-later.html", context)

	def post(self, request):
		stored_posts = request.session.get("stored_posts")
		if stored_posts is None:
			stored_posts = []
		post_id = int(request.POST["post_id"])

		if post_id not in stored_posts:
			stored_posts.append(post_id)
			request.session["stored_posts"] = stored_posts
		return HttpResponseRedirect("/")
