from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator
from taggit.models import Tag

from django.contrib.postgres.search import SearchVector
from .forms import SearchForm

def post_list(request, tag_slug=None):
    posts = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    return render(request,
                'jobs/post/list.html',
                {'posts': posts,
                 'tag': tag})


def post_detail(request, id):
    try:
        post = Post.published.get(id=id)

    except Post.DoesNotExist:
        raise Http404("No Post found.")
    
    return render(request,
                'jobs/post/detail.html',
                {'post': post})


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        results = Post.published.annotate(
            search=SearchVector('title', 'body'),
        ).filter(search=query)
    return render(request, 'jobs/post/search.html', {'form': form,
                                                     'query': query,
                                                     'results': results})