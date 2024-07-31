from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import *
from .forms import ArticleCreateForm, CommentCreateForm, EmailArticleForm
from .filters import ArticleFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.mail import send_mail
# Create your views here.

def home(request):
    articles = Article.published.all()
    return render(request, 'article/home.html', {'articles':articles})

@login_required
def article_list(request, tag=None):
    article_filter = ArticleFilter(request.GET, queryset=Article.published.all())
    if tag:
        articles = Article.published.filter(tags__slug=tag)
    else:
        article_list = article_filter.qs
        paginator = Paginator(article_list, 5) # Show 25
        page_number = request.GET.get('page')
        try:
            articles = paginator.page(page_number)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            articles = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            articles = paginator.page(paginator.num_pages)
    context = {
        'articles': articles,
        'filter': article_filter,
    }
    return render(request, 'article/article_list.html', context)

@login_required
def article_detail(request, year, month, day, article, pk):
    article = get_object_or_404(Article, pk=pk, status=Article.Status.PUBLISHED, slug=article, publish__year=year, publish__month=month, publish__day=day)
    commentform = CommentCreateForm()
    context ={
        'article': article,
        'commentform':commentform
    }
    return render(request, 'article/article_detail.html', context)

@login_required
def comment_sent(request, pk):
    article = get_object_or_404(Article, id=pk)
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_article = article
            comment.save()
    
    return render(request, 'includes/comment.html', {'comment':comment})

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, id=pk, author=request.user)
    parent_article_id = comment.parent_article.id
    comment.delete()
    messages.success(request, 'Comment deleted')
    return redirect('article:article', parent_article_id)
    

@login_required
def create_article(request):
    form = ArticleCreateForm()
    if request.method == 'POST':
        form = ArticleCreateForm(request.POST, request.FILES)
        if form.is_valid:
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, "Your article has been created!")
            return redirect('article:article_list')
    else:
        form = ArticleCreateForm()
    return render(request, 'article/create.html', {'form':form})

@login_required
def article_update(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleCreateForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article:article_list')
    else:
        form = ArticleCreateForm(instance=article)
    return render(request, 'article/create.html', {'form': form})

@login_required
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    return redirect('article:article_list') 


@login_required
def article_share(request, article):
    # Retrieve post by id
    article = get_object_or_404(Article, slug=article, status=Article.Status.PUBLISHED)
    sent = False
    
    if request.method == 'POST':
    # Form was submitted
        form = EmailArticleForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # ... send email
            article_url = request.build_absolute_uri(
            article.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
            f"{article.title}"
            message = f"Read {article.title} at {article_url}\n\n" \
            f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'Hensonasaiah21@gmail.com',
            [cd['to']])
            sent = True
    else:
        form = EmailArticleForm()
    return render(request, 'article/share.html', {'article': article, 'form':form, 'sent':sent })

def love_article(request, pk):
    article = get_object_or_404(Article, id=pk)
    user_exist = article.love.filter(username=request.user.username).exists()
   
    if article.author != request.user:
        if user_exist:
            article.love.remove(request.user)
        else:
            article.love.add(request.user)

    return HttpResponse( article.love.count() )

@login_required
def like_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    user_exist = comment.likes.filter(username=request.user.username).exists()
   
    if comment.author != request.user:
        if user_exist:
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)

    return HttpResponse( comment.likes.count() )

@login_required
def dislike_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    user_exist = comment.dislikes.filter(username=request.user.username).exists()
   
    if comment.author != request.user:
        if user_exist:
            comment.dislikes.remove(request.user)
        else:
            comment.dislikes.add(request.user)

    return HttpResponse( comment.dislikes.count() )