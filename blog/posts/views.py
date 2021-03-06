from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from comments.forms import CommentForm
from comments.models import Comment
from .models import Post
from .forms import PostForm


def post_create(request):
    if not request.user.is_authenticated():
        messages.success(request, 'User is not logged in.')
        return redirect('posts:list')
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

    if post.draft or post.publish > timezone.now().date():
        user = request.user
        if not user.is_staff or not user.is_superuser:
            raise Http404

    initial_data = {
        'content_type': post.content_type,
        'object_id': post.id,
    }
    comment_form = CommentForm(request.POST or None, initial=initial_data)

    if comment_form.is_valid():

        # Users must be logged in to comment
        if not request.user.is_authenticated():
            messages.success(request, 'User is not logged in.')
            return HttpResponseRedirect(reverse('posts:detail', args=(post.id,)))

        parent_obj = None
        c_type = comment_form.cleaned_data.get('content_type')
        try:
            parent_id = int(request.POST.get('parent_id'))
        except TypeError:
            parent_id = None

        # Store the parent id if we are processing a reply
        # Confirm that the parent comment exists in the DB
        if parent_id:
            queryset = Comment.objects.filter(id=parent_id)
            if queryset.exists():
                parent_obj = queryset.first()

        Comment.objects.get_or_create(
            user=request.user,
            content_type=ContentType.objects.get(model=c_type),
            object_id=comment_form.cleaned_data.get('object_id'),
            content=comment_form.cleaned_data.get('content'),
            parent=parent_obj,
        )

        return HttpResponseRedirect(reverse('posts:detail', args=(post.id,)))

    context = {
        'post': post,
        'comment_form': comment_form,
    }
    return render(request, 'posts/detail.html', context)


def post_list(request):
    today = timezone.now().date()
    posts = Post.objects.active()

    # Staff can see everything
    user = request.user
    if user.is_staff or user.is_superuser:
        posts = Post.objects.all()

    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()

    paginator = Paginator(posts, 6)  # Show 6 contacts per page
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
        'posts': posts_per_page,
        'today': today,
    }
    return render(request, 'posts/post_list.html', context)


def post_edit(request, slug):
    if not request.user.is_authenticated():
        messages.success(request, 'User is not logged in.')
        return redirect('posts:list')
    post = get_object_or_404(Post, pk=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, 'Post updated.')
        return HttpResponseRedirect(reverse('posts:detail', args=(post.id,)))

    context = {
        'post': post,
        'form': form,
    }

    return render(request, 'posts/post_form.html', context=context)


def post_delete(request, slug):
    if not request.user.is_authenticated():
        messages.success(request, 'User is not logged in.')
        return redirect('posts:list')
    post = get_object_or_404(Post, pk=slug)
    post.delete()
    messages.success(request, 'Post deleted successfully.')
    return redirect('posts:list')
