from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Post, Group
from django.shortcuts import render



# Create your views here.
# Главная страница


def index(request):
    # post_list = Post.objects.all().order_by('-pub_date')
    # Если порядок сортировки определен в классе Meta модели,
    # запрос будет выглядить так:
    post_list = Post.objects.all()
    # Показывать по 10 записей на странице.
    paginator = Paginator(post_list, 10) 

    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get('page')

    # Получаем набор записей для страницы с запрошенным номером
    page_obj = paginator.get_page(page_number)
    # Отдаем в словаре контекста
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


# Страница с постами группы
def group_posts(request, slug):
    template = 'posts/group_list.html'
    # Функция get_object_or_404 получает по заданным критериям объект
    # из базы данных или возвращает сообщение об ошибке, если объект не найден.
    # В нашем случае в переменную group будут переданы объекты модели Group,
    # поле slug у которых соответствует значению slug в запросе
    group = get_object_or_404(Group, slug=slug)
    # Метод .filter позволяет ограничить поиск по критериям.
    # Это аналог добавления
    # условия WHERE group_id = {group_id}
    # posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    group_posts = group.posts.all()
    paginator = Paginator(group_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        #'group': group,
        #'posts': posts,
        'page_obj': page_obj,
    }   
    return render(request, template, context)


# Профиль пользователя
def profile(request, username):
    template = 'post/profile.html'
    # Здесь код запроса к модели и создание словаря контекста
    #profile_user = 
    #post_count = 
        
    # Блок пажинатора
    posts_user =  Post.objects.filter(author=username)
    paginator = Paginator(posts_user, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Создание словаря контекста
    context = {
        'profile_user' : profile_user,
        'post_count': post_count,
        'page_obj': page_obj,
        # 'page_obj': page_obj
    }
    return render(request, template, context)

# Посты пользователя
def post_detail(request, post_id):
    
    # Здесь код запроса к модели и создание словаря контекста
    post = get_object_or_404(Post,pk=post_id)
    pub_date = post.pub_date
    post_title = post.text[:30]
    author = post.author
    author_posts = author.posts.all().count()
    post_group_title= post.group
    context = {
        "post":post,
        "post_title": post_title,
        "author" : author,
        "author_posts": author_posts,
        "pub_date": pub_date,
        "post_group_title": post_group_title, 
    }
    template = 'posts/post_detail.html'
    return render(request, template, context)

