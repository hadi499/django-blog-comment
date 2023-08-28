from django.shortcuts import render, redirect
from .models import BlogPost, Comment
from .forms import CommentForm, PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator


@login_required
def home(request):
    if 'q' in request.GET:
        q = request.GET['q']
        result = Q(title__icontains=q)
        posts = BlogPost.objects.filter(result)
    else:
        data = BlogPost.objects.all()
        paginator = Paginator(data, 4)  # 10 item per halaman
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)
    context = {
        'posts': posts
    }

    return render(request, 'blog/home.html', context)

# @login_required
# def home(request):
#     posts = BlogPost.objects.all()
#     return render(request, 'blog/home.html', {'posts': posts})


@login_required
def createPost(request):
    form = PostForm(request.POST, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid:
            form.save()
            return redirect('home')
    return render(request, 'blog/create.html', {'form': form})


@login_required
def deletePost(request, pk):
    if request.method == 'POST':
        post = BlogPost.objects.get(pk=pk)
        post.delete()
    return redirect('home')


@login_required
def blog_detail(request, pk):
    post = BlogPost.objects.get(id=pk)
    side_posts = BlogPost.objects.exclude(id=pk)
    comments = Comment.objects.filter(post=post)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user  # Assuming user authentication is implemented
            comment.save()
            form = CommentForm()  # Clear the form after submission
            return redirect('detail', pk=post.id)
    else:
        form = CommentForm()
    return render(request, 'blog/detail.html', {'post': post, 'comments': comments, 'form': form, 'side_posts': side_posts})


@login_required
def updatePost(request, pk):
    post = BlogPost.objects.get(id=pk)
    data = {
        'title': post.title,
        'content': post.content,
        'image': post.image,
        'author': post.author
    }
    form = PostForm(request.POST or None, request.FILES or None,
                    initial=data, instance=post)
    if request.method == 'POST':
        if form.is_valid:
            form.save()
            return redirect('home')
    return render(request, 'blog/update.html', {'form': form})
