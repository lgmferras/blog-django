from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User


PER_PAGE = 9


# Create your views here.
def index(request):
    posts = Post.objects.get_published()

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Home',
        'page_obj': page_obj,

    }
    return render(request, 'blog/pages/index.html', context)

def page(request,slug):
    page = Page.objects.filter(is_published=True).filter(slug=slug).first()
    context = {
        'title': 'Page',
        'page': page,
    }
    return render(request, 'blog/pages/page.html', context)

def post(request,slug):
    post = Post.objects.get_published().filter(slug=slug).first()
    context = {
        'title': 'Post',
        'post': post,
    }
    return render(request, 'blog/pages/post.html', context)

def created_by(request, author_pk):
    user = User.objects.get(pk=author_pk)
    posts = Post.objects.get_published().filter(created_by__pk=author_pk)
    page_title = f'Created by {user.first_name} {user.last_name}'

    if user is None:
        raise Http404()

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
            'page_obj': page_obj,
            'title': page_title,
            
    }
    return render(
        request,
        'blog/pages/index.html',
        context
    )



def created_at(request, created_at):
    posts = Post.objects.get_published().filter(created_at=created_at)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    if len(page_obj) == 0:
        raise Http404()
    
    page_title = f'Created at {created_at[:10]}'
    
    context = {
            'page_obj': page_obj,
            'title': page_title,
    }
    return render(
        request,
        'blog/pages/index.html',
        context
    )

def category(request, slug):
    posts = Post.objects.get_published().filter(category__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404()
    
    page_title = f'Category: {slug}'

    context = {
            'page_obj': page_obj,
            'title': page_title,
    }
    return render(
        request,
        'blog/pages/index.html',
        context
    )

def tag(request, slug):
    posts = Post.objects.get_published().filter(tags__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    if len(page_obj) == 0:
        raise Http404()
    
    page_title = f'Tag: {slug}'

    context = {
            'page_obj': page_obj,
            'title': page_title,
    }
    return render(
        request,
        'blog/pages/index.html',
        context
    )

def search(request):
    search_value = request.GET.get('search').strip()
    posts = Post.objects.get_published().filter(
        Q(title__icontains=search_value) |
        Q(content__icontains=search_value) |
        Q(excerpt__icontains=search_value)
    )[:PER_PAGE]

    if len(posts) == 0:
        raise Http404()
    
    page_title = f'Search: {search_value}'

    context = {
            'page_obj': posts,
            'search_value': search_value,
            'title': page_title,
    }
    return render(
        request,
        'blog/pages/index.html',
        context
    )
    