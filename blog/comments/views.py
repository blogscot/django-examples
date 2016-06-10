from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404


from . forms import CommentForm
from . models import Comment


def comment_thread(request, id):
    comment = get_object_or_404(Comment, pk=id)

    initial_data = {
        'content_type': comment.content_type,  # associated post instance
        'object_id': comment.object_id,        # post id
    }

    form = CommentForm(request.POST or None, initial=initial_data)

    if form.is_valid():
        # Users must be logged in to comment
        if not request.user.is_authenticated():
            messages.success(request, 'User is not logged in.')
            return HttpResponseRedirect(reverse('comments:thread', args=(comment.id,)))

        parent_obj = None
        c_type = form.cleaned_data.get('content_type')
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
            object_id=form.cleaned_data.get('object_id'),
            content=form.cleaned_data.get('content'),
            parent=parent_obj,
        )

        return HttpResponseRedirect(reverse('comments:thread', args=(comment.id,)))

    context = {
        'form': form,
        'comment': comment,
    }

    return render(request, 'comment_thread.html', context)


