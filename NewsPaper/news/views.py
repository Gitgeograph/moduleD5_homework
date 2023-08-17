from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from .filters import PostFilter
from .forms import PostForm
from .models import Post, Author
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin



class PostList(ListView):
    model = Post
    ordering = ['-creationData']
    template_name = 'post/posts.html'
    context_object_name = 'posts'
    paginate_by = 2

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)
    

class PostSearch(ListView):
    model = Post
    ordering = ['-creationData']
    template_name = 'post/post_search.html'
    context_object_name = 'post_search'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset = self.get_queryset())
        context['form'] = PostForm()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post/post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'post/post_create.html'
    permission_required = ('news.add_post',
                            'news.change_post')
    permission_denied_message = 'Чтобы создавать новости, необходимо стать автором'
    form_class = PostForm


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'post/post_create.html'
    permission_required = ('news.add_post',
                            'news.change_post')
    permission_denied_message = 'Чтобы редактировать новости, необходимо стать автором'
    form_class = PostForm

    def get_object(self, **kwargs):
       id = self.kwargs.get('pk')
       return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'post/post_delete.html'
    queryset = Post.objects.all()
    success_url = reverse_lazy('news:all_posts')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context
    
@login_required
def upgrade_me(request):
    user = request.user
    Author.objects.create(authorUser=user)
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/news/')


class HomeView(TemplateView):
    template_name = 'post/home_page.html'