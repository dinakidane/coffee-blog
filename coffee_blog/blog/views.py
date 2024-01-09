from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Like
from .forms import CommentForm
from django.contrib.auth.decorators import login_required

# blog/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Like
from .forms import CommentForm
from django.contrib.auth.decorators import login_required

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    likes = post.likes.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'likes': likes, 'comment_form': comment_form})

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(post=post, user=request.user)

    if not created:
        like.delete()

    return redirect('post_detail', pk=post.pk)
