from re import template
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Post, Group, User
from django.shortcuts import render, redirect
from .forms import PostForm
from django.views.generic.edit import CreateView



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
        'page_obj': page_obj,
    }   
    return render(request, template, context)


# Профиль пользователя

def profile(request, username):
    template = 'posts/profile.html'
    user404=get_object_or_404(User, username=username)
    user_posts = get_list_or_404(Post, author__username=username)
    user_posts_count = user404.posts.select_related('author').count()

    page = Paginator(user_posts, 10)
    page_number = request.GET.get('page')
    page_obj = page.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'user404': user404,
        'user_posts_count': user_posts_count,

                           
    }
    return render(request, template, context)

# Посты пользователя
def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, id=post_id)
    title = post.text[:30]
    username = get_object_or_404(User, id=post.author_id)
    count_of_posts = Post.objects.filter(author=username).count()
    posts_of_author = Post.objects.filter(author=username)
    context = {
        'post' : post,
        'post.text': post.text,
        'title' : title,
        'username':username,
        'count_of_posts': count_of_posts,
        'group': post.group,
        'posts_of_author': posts_of_author,

    }
    return render(request, template, context)


class PostView(CreateView):
    form_class = PostForm

    template_name = 'posts/create_post.html'

    success_url = '/profile/<username>/'   #Проверь ссылку 


def post_create(request):
    template_name = 'posts/create_post.html'
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile/', post.author)
        return render (request, template_name, {'form':form})
    form = PostForm()
    return render(request, template_name, {'form':form})
