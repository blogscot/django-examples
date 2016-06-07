from urllib.parse import quote_plus

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from .models import Post
from .forms import PostForm


def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Post created successfully.')
        return redirect('posts:list')

    context = {
        'form': form,
    }
    return render(request, 'posts/post_form.html', context=context)


def post_detail(request, slug):
    post = get_object_or_404(Post, pk=slug)
    share_string = quote_plus(post.content)
    context = {
        'post': post,
        'share_string': share_string,
    }
    return render(request, 'posts/detail.html', context)


def post_list(request):
    posts = Post.objects.all()

    paginator = Paginator(posts, 6)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        posts_per_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts_per_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts_per_page = paginator.page(paginator.num_pages)

    context = {
        'posts': posts_per_page
    }
    return render(request, 'posts/post_list.html', context)


def post_edit(request, slug):
    post = get_object_or_404(Post, pk=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Post updated.')
        return HttpResponseRedirect(reverse('posts:detail', args=(post.id,)))

    context = {
        'post': post,
        'form': form,
    }

    return render(request, 'posts/post_form.html', context=context)


def post_delete(request, slug):
    post = get_object_or_404(Post, pk=slug)
    post.delete()
    messages.success(request, 'Post deleted successfully.')
    return redirect('posts:list')
