from django.core.paginator import Paginator
from django.shortcuts import render
from blog.models import Post
from django.db.models import Q

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
    context = {
        'title': 'Page',
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
    posts = Post.objects.get_published().filter(created_by__pk=author_pk)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
            'page_obj': page_obj,
            'title': 'Created by',
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
    context = {
            'page_obj': page_obj,
            'title': 'Created at',
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
    context = {
            'page_obj': page_obj,
            'title': 'Category',
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
    context = {
            'page_obj': page_obj,
            'title': 'Tags',
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

    context = {
            'page_obj': posts,
            'search_value': search_value,
            'title': 'Search',
    }
    return render(
        request,
        'blog/pages/index.html',
        context
    )
    