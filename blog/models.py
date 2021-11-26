from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE

class Tag(models.Model):
	caption = models.CharField(max_length=20)
	def __str__(self):
		return self.caption

class Author(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	def __str__(self):
		return f"{self.first_name}"

class Post(models.Model):
	slug = models.SlugField(unique=True, db_index=True)
	# image = models.CharField(max_length=500)
	image = models.ImageField(upload_to='posts', null=True)
	# author = models.CharField(max_length=500)
	author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
	date = models.DateField()
	title = models.CharField(max_length=500)
	excerpt = models.CharField(max_length=500)
	content = models.TextField(max_length=500)
	tags = models.ManyToManyField(Tag)
	def __str__(self):
		return self.title


class Comment(models.Model):
	user_name = models.CharField(max_length=50)
	user_email = models.EmailField()
	content = models.TextField(max_length=200)
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")