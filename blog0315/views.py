'''blog1209/views.py'''

from django.http import HttpResponse
from django.shortcuts import render
from . models import Article,Category,Tag,ReadNum
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404,JsonResponse
from django.urls import reverse
from .forms import ArticleForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from comment.models import Comment
from comment.form import CommentForm
from django.contrib.contenttypes.models import ContentType


def All_list(request):
    article_all = Article.objects.all().order_by('-created_time')
    article_list3 = article_all[0:3]
    category_list = Category.objects.all()
    tag_list = Tag.objects.all()
    ######分页
    paginator = Paginator(article_all,7)
    page_num = request.GET.get('page', 1)  # 获取url的页面参数（GET请求）
    page_of_articles = paginator.get_page(page_num)
    currentr_page_num = page_of_articles.number  # 获取当前页码
    # 获取当前页码前后各2页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)


def index(request):
    article_list = Article.objects.all().order_by('-created_time')
    article_list3 = article_list[0:3]
    category_list = Category.objects.all()
    tag_list = Tag.objects.all()
    ####分页
    paginator = Paginator(article_list, 7)
    page_num = request.GET.get('page', 1)  # 获取url的页面参数（GET请求）
    page_of_articles = paginator.get_page(page_num)
    currentr_page_num = page_of_articles.number  # 获取当前页码
    # 获取当前页码前后各2页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    context = {'article_list': page_of_articles,'article_list3': article_list3,'category_list':category_list,'tag_list':tag_list}
    context['page_of_blogs'] = page_of_articles
    context['page_range'] = page_range
    return render(request, 'blog0315/index.html', context)


def about(request):
    article_all = Article.objects.all().order_by('-created_time')
    article_list3 = article_all[0:3]
    category_list = Category.objects.all()
    tag_list = Tag.objects.all()
    context = { 'article_list3': article_list3, 'category_list': category_list,
               'tag_list': tag_list}
    return render(request, 'blog0315/about.html',context)


def contact(request):
    article_all = Article.objects.all().order_by('-created_time')
    article_list3 = article_all[0:3]
    category_list = Category.objects.all()
    tag_list = Tag.objects.all()
    context = { 'article_list3': article_list3, 'category_list': category_list,
               'tag_list': tag_list}
    return render(request, 'blog0315/contact.html',context)


@login_required
def blogs(request):
    '''显示单个用户自己的博客'''
    article_all = Article.objects.all().order_by('-created_time')
    article_list3 = article_all[0:3]
    category_list = Category.objects.all()
    tag_list = Tag.objects.all()
    article_list = Article.objects.filter(author=request.user).order_by('-created_time')
    ####分页
    #context['page_of_blogs'] = page_of_articles
    #context['page_range'] = page_range
    #文章列表改为page_of_articles
    paginator = Paginator(article_list, 7)
    page_num = request.GET.get('page', 1)  # 获取url的页面参数（GET请求）
    page_of_articles = paginator.get_page(page_num)
    currentr_page_num = page_of_articles.number  # 获取当前页码
    # 获取当前页码前后各2页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    context = {'article_list': page_of_articles, 'article_list3': article_list3, 'category_list': category_list,
               'tag_list': tag_list}
    context['page_of_blogs'] = page_of_articles
    context['page_range'] = page_range
    return render(request, 'blog0315/blogs.html',context)


def selfblog(request, article_author):
    '''显示某个用户的博客'''
    #article = Article.objects.get(id=article_id)
    #article_author = article.author
    article_all = Article.objects.all().order_by('-created_time')
    article_list3 = article_all[0:2]
    category_list = Category.objects.all()
    tag_list = Tag.objects.all()
    author = User.objects.get(username=article_author)
    article_list = Article.objects.filter(author=author.id).order_by('-created_time')
    ####分页
    # context['page_of_blogs'] = page_of_articles
    # context['page_range'] = page_range
    # 文章列表改为page_of_articles
    paginator = Paginator(article_list, 7)
    page_num = request.GET.get('page', 1)  # 获取url的页面参数（GET请求）
    page_of_articles = paginator.get_page(page_num)
    currentr_page_num = page_of_articles.number  # 获取当前页码
    # 获取当前页码前后各2页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context = {'article_list': page_of_articles, 'article_list3': article_list3, 'category_list': category_list,
               'tag_list': tag_list}
    context['page_of_blogs'] = page_of_articles
    context['page_range'] = page_range
    return render(request, 'blog0315/selfblog.html',context)


def article_detail(request, article_id):
    """显示单个文章"""
    article_all = Article.objects.all().order_by('-created_time')
    article_list3 = article_all[0:3]
    category_list = Category.objects.all()
    tag_list = Tag.objects.all()
    article = Article.objects.get(id=article_id)
    previous_article = Article.objects.filter(created_time__gt=article.created_time).last()
    next_article = Article.objects.filter(created_time__lt=article.created_time).first()
    #评论相关
    article_content_type = ContentType.objects.get_for_model(article)
    comments = Comment.objects.filter(content_type=article_content_type, object_id=article.id)
    data = {}
    data['content_type'] =article_content_type.model
    data['object_id'] = article_id
    context = {'article':article,'previous_article':previous_article,'next_article':next_article,
                'article_list3': article_list3, 'category_list': category_list,
               'tag_list': tag_list
               }
    context['comment_form'] = CommentForm(initial=data)
    context['comments'] = comments
    if not request.COOKIES.get('article_%s_read' % article_id):
        if ReadNum.objects.filter(article=article).count():  # 判断对应博客的记录是否存在
            #  存在记录
            readnum = ReadNum.objects.get(article=article)  # 取出数量
        else:
            # 不存在记录
            readnum = ReadNum(article=article)  # 实例化
        readnum.read_num += 1
        readnum.save()
    render_x = render(request, 'blog0315/article_detail.html', context)
    render_x.set_cookie('article_%s_read' % article_id,'true')
    return render_x


@login_required
def new_article(request):
    """添加文章"""
    article_all = Article.objects.all().order_by('-created_time')
    article_list3 = article_all[0:3]
    category_list = Category.objects.all()
    tag_list = Tag.objects.all()
    article_form = ArticleForm(request.POST)
    if request.method == 'POST':
        # article_form = ArticleForm(request.POST)
        if article_form.is_valid():
            article = Article()
            article.author = request.user
            article.title = request.POST['title']
            #body
            body = request.POST['body']
            # body = body[3:]
            # body_count = len(body)
            # body1 = body[:body_count-6]
            # body2 = body[body_count-2:]
            # body = body1+body2
            #
            article.body = body
            article.category = Category.objects.filter(id=request.POST['category'])[0]
            article.save()
            tagslist = request.POST.getlist('tags')
            for i in tagslist:
                article.tags.add(Tag.objects.get(id=i))
            article.save()
    # if request.method == 'POST':
    #     article = Article()
    #     article.author = request.user
    #     article.title = request.POST['title']
    #     article.body = request.POST['body']
    #     article.category = Category.objects.filter(name=request.POST['category'])[0]
    #     article.save()
    #     if request.POST['tags'] != '':
    #         article.tags.add(Tag.objects.get(name=request.POST['tags']))
    #         article.save()
        return HttpResponseRedirect(reverse('blog0315:index'))

    context = {'article_list3': article_list3, 'category_list': category_list,
               'tag_list': tag_list,'article_form':article_form}
    return render(request, 'blog0315/new_article.html', context)


def article_category(request, category_id):
    '''显示某个分类的博客'''
    article_all = Article.objects.all().order_by('-created_time')
    article_list3 = article_all[0:3]
    category_list = Category.objects.all()
    tag_list = Tag.objects.all()
    category_name = Category.objects.get(id=category_id)
    article_list = Article.objects.filter(category=category_name).order_by('-created_time')
    ####分页
    # context['page_of_blogs'] = page_of_articles
    # context['page_range'] = page_range
    # 文章列表改为page_of_articles
    paginator = Paginator(article_list, 7)
    page_num = request.GET.get('page', 1)  # 获取url的页面参数（GET请求）
    page_of_articles = paginator.get_page(page_num)
    currentr_page_num = page_of_articles.number  # 获取当前页码
    # 获取当前页码前后各2页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context ={'article_list':page_of_articles,'article_list3': article_list3, 'category_list': category_list,
               'tag_list': tag_list}
    context['page_of_blogs'] = page_of_articles
    context['page_range'] = page_range
    return render(request, 'blog0315/article_category.html',context)


def article_tag(request, tag_id):
    '''显示某个标签的博客'''
    article_all = Article.objects.all().order_by('-created_time')
    article_list3 = article_all[0:3]
    tag_list = Tag.objects.all()
    category_list = Category.objects.all()
    tag_name = Tag.objects.get(id=tag_id)
    article_list = Article.objects.filter(tags=tag_name).order_by('-created_time')
    ####分页
    # context['page_of_blogs'] = page_of_articles
    # context['page_range'] = page_range
    # 文章列表改为page_of_articles
    paginator = Paginator(article_list, 7)
    page_num = request.GET.get('page', 1)  # 获取url的页面参数（GET请求）
    page_of_articles = paginator.get_page(page_num)
    currentr_page_num = page_of_articles.number  # 获取当前页码
    # 获取当前页码前后各2页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context ={'article_list':page_of_articles,'article_list3': article_list3, 'category_list': category_list,
               'tag_list': tag_list}
    context['page_of_blogs'] = page_of_articles
    context['page_range'] = page_range
    return render(request, 'blog0315/article_tag.html',context)


def classified(request,year,month):
    article_list = Article.objects.filter(created_time__year=year, created_time__month=month)
    context = {'article_list': article_list}
    return render('blog0315/article_with_date.html', context)


def test(request):
    article_form = ArticleForm()
    context = {'article_form': article_form}
    return render(request,'blog0315/test.html', context)


def test2(request,article_id):
    article_list = Article.objects.get(id=article_id)
    context = {'article_list': article_list}
    return render('blog0315/test2.html', context)

# Create your views here.

#
# def login(request):
#     try:
#         data = request.POST.get('bool')
#         return JsonResponse({'static': 'true'})
#     except:
#         return JsonResponse({'static': 'False'})

