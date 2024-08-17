from django.core.paginator import Paginator
from django.shortcuts import render

posts = list(range(1000))

# Create your views here.
def index(request):
    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Home',
        'page_obj': page_obj,

    }
    return render(request, 'blog/pages/index.html', context)

def page(request):
    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Page',
    }
    return render(request, 'blog/pages/page.html', context)

def post(request):
    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Post',
    }
    return render(request, 'blog/pages/post.html', context)