from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Article
from django.db.models import Q

# Create your views here.


def Articlespage(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    print(q)

    items = Article.objects.filter(
        Q(title__icontains=q)
    )

    paginator = Paginator(items, 6)  # Show 10 items per page
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    context = {
        'items': items,
    }

    return render(request, 'article/index.html', context)


def article(request, pk):
    article = Article.objects.get(id=pk)


    context = {'article': article}
    return render(request, 'article/article.html', context)
