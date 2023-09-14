from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, FormView, CreateView, TemplateView
from django.views.generic.edit import FormMixin

from blog.models import Post, Comment, User
from blog.views.forms import PostModelForm, CommentForm
from blog import constant


class PostListView(ListView):
    model = Post
    ordering = ['-created_at']
    paginate_by = constant.PAGINATION_PER_PAGE

    def get_queryset(self):
        search = self.request.GET.get('search')
        if search:
            object_list = self.model.objects.filter(approved=True, title__icontains=search)
        else:
            object_list = self.model.objects.filter(approved=True)
        return object_list


class PostDetailView(FormMixin, DetailView):
    model = Post
    context_object_name = 'post'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        comments = Comment.objects.filter(post_id=self.object.pk).order_by('-created_at')
        context = super().get_context_data(**kwargs)
        context['comments'] = comments
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('blog/post_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.post_id = self.object
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class CreatePostView(CreateView):
    template_name = 'blog/post_form.html'
    form_class = PostModelForm

    def form_valid(self, form):
        user = self.request.user
        if user.is_anonymous:
            form.instance.user = User.objects.get(pk=constant.ANOMYNOUS_USER_ID)
        else:
            form.instance.user = user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog/post_list')


class AboutView(TemplateView):
    template_name = "about.html"


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/home')

