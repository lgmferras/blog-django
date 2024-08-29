from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from typing import Any
# from django.db.models.query import QuerySet



PER_PAGE = 9



# def index(request):
#     posts = Post.objects.get_published()

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#     context = {
#         'title': 'Home',
#         'page_obj': page_obj,

#     }
#     return render(request, 'blog/pages/index.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    ordering = '-pk',
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        return context

# def created_by(request, author_pk):
#     user = User.objects.get(pk=author_pk)
#     posts = Post.objects.get_published().filter(created_by__pk=author_pk)
#     page_title = f'Created by {user.first_name} {user.last_name}'

#     if user is None:
#         raise Http404()

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#     context = {
#             'page_obj': page_obj,
#             'title': page_title,
            
#     }
#     return render(
#         request,
#         'blog/pages/index.html',
#         context
#     )

class CreatedByListView(PostListView):
    def get_queryset(self):
        author_pk = self.kwargs['author_pk']
        if not User.objects.filter(pk=author_pk).exists():
            raise Http404(f"User with pk={author_pk} does not exist.")
        return Post.objects.get_published().filter(created_by__pk=author_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.kwargs['author_pk'])
        context['title'] = f'Created by {user.first_name} {user.last_name}'
        return context

# def page(request,slug):
#     page = Page.objects.filter(is_published=True).filter(slug=slug).first()
#     context = {
#         'title': 'Page',
#         'page': page,
#     }
#     return render(request, 'blog/pages/page.html', context)

class PageDetailView(DetailView):
    model = Page
    template_name = 'blog/pages/page.html'
    context_object_name = 'page'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        # Filtra apenas páginas publicadas
        return Page.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Page'
        return context

# def post(request,slug):
#     post = Post.objects.get_published().filter(slug=slug).first()
#     context = {
#         'title': 'Post',
#         'post': post,
#     }
#     return render(request, 'blog/pages/post.html', context)

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/pages/post.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        # Filtra apenas posts publicados
        return Post.objects.get_published()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Post'
        return context

# def created_at(request, created_at):
#     posts = Post.objects.get_published().filter(created_at=created_at)

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
    
#     if len(page_obj) == 0:
#         raise Http404()
    
#     page_title = f'Created at {created_at[:10]}'
    
#     context = {
#             'page_obj': page_obj,
#             'title': page_title,
#     }
#     return render(
#         request,
#         'blog/pages/index.html',
#         context
#     )

class CreatedAtListView(PostListView):
    def get_queryset(self):
        created_at = self.kwargs['created_at']
        return Post.objects.get_published().filter(created_at=created_at)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Created at {self.kwargs["created_at"][:10]}'
        return context
        

# def category(request, slug):
#     posts = Post.objects.get_published().filter(category__slug=slug)

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     if len(page_obj) == 0:
#         raise Http404()
    
#     page_title = f'Category: {slug}'

#     context = {
#             'page_obj': page_obj,
#             'title': page_title,
#     }
#     return render(
#         request,
#         'blog/pages/index.html',
#         context
#     )

class CategoryListView(PostListView):
    allow_empty = False
    def get_queryset(self):
        return Post.objects.get_published().filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Category: {self.kwargs["slug"]}'
        return context

# def tag(request, slug):
#     posts = Post.objects.get_published().filter(tags__slug=slug)

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
    
#     if len(page_obj) == 0:
#         raise Http404()
    
#     page_title = f'Tag: {slug}'

#     context = {
#             'page_obj': page_obj,
#             'title': page_title,
#     }
#     return render(
#         request,
#         'blog/pages/index.html',
#         context
#     )

class TagListView(PostListView):
    def get_queryset(self):
        return Post.objects.get_published().filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Tag: {self.kwargs["slug"]}'
        return context

# def search(request):
#     search_value = request.GET.get('search').strip()
#     posts = Post.objects.get_published().filter(
#         Q(title__icontains=search_value) |
#         Q(content__icontains=search_value) |
#         Q(excerpt__icontains=search_value)
#     )[:PER_PAGE]

#     if len(posts) == 0:
#         raise Http404()
    
#     page_title = f'Search: {search_value}'

#     context = {
#             'page_obj': posts,
#             'search_value': search_value,
#             'title': page_title,
#     }
#     return render(
#         request,
#         'blog/pages/index.html',
#         context
#     )

class SearchListView(PostListView):
    def get_queryset(self):
        search_value = self.request.GET.get('search').strip()
        return Post.objects.get_published().filter(
            Q(title__icontains=search_value) |
            Q(content__icontains=search_value) |
            Q(excerpt__icontains=search_value)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_value'] = self.request.GET.get('search').strip()
        context['title'] = f'Search: {context["search_value"]}'
        return context
    