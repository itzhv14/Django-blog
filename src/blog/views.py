from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView,
	)
from .models import Post
from django.contrib.auth.models import User


def home(request):

	context = {
		'posts': Post.objects.all(),
	}
	return render(request, "blog/home.html", context)


class PostListView(ListView):
	model = Post
	context_object_name = 'posts' # coz we r using post as the variable in home template and default var is object_list
	template_name = 'blog/home.html' # default is <app>/<model>_<viewtype>.html
	ordering = ['-date_posted'] # to change the order of the list on home page as per the date
	# - minus coz we want newset to oldest
	paginate_by = 5


class UserPostListView(ListView):
	model = Post
	context_object_name = 'posts'
	template_name = 'blog/user_posts.html'
	paginate_by = 5

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username')) # to get username from url and kwargs is query parameters
		return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
	model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		else:
			return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		else:
			return False


def about(request):
	return render(request, "blog/about.html",{'title': 'About'})
