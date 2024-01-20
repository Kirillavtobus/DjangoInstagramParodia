from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from .forms import RegistrationForm, LoginForm, PostForm, ProfilForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from .models import Post, Following, Profile


def home(request):
    users = User.objects.all()
    foll = Following.objects.all()
    user = request.user
    username = user.id
    posts = Post.objects.filter(user=username)
    return render(request, 'home.html', {'posts': posts, 'foll': foll})


def page_2(request, **kwargs):
    search_query = request.GET.get('q', None)
    if search_query:
        users = User.objects.filter(username__icontains=search_query)
    else:
        users = User.objects.all()
    user = request.user
    context = {'user': user, 'users': users}
    return render(request, 'page_2.html', {'user': user, 'users': users})


def RegistrationView(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            user_foll = User.objects.get(username=username)
            following_user = Following(user=user_foll)
            following_user.save()
            return redirect('page_2')
    else:
        form = RegistrationForm()
        return render(request, 'registration.html', {'form': form})


class LoginPage(LoginView):
    template_name = 'login.html'
    form_class = LoginForm
    redirect_authenticated_user = True


def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('page_2')
            else:
                return redirect('/login')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def get_success_url(self):
        return 'page_2'


@login_required
def ProfileView(request, **kwargs):
    user = request.user
    foll = Following.objects.get(user=user)
    profile = Profile.objects.filter(user=user)
    return render(request, 'profile.html', {'user': user, 'foll': foll, 'profile': profile})


def handle_upload_file(f):
    with open(f'djangoSemestr_app/static/{f.name}', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)




def PostCreateView(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        users = User.objects.all()
        user = request.user
        user_id = user.id
        if form.is_valid():
            about = form.cleaned_data['about']
            image = form.cleaned_data['image']
            user = User.objects.get(id=user_id)
            post = Post(about=about, image=image, user=user)
            # handle_upload_file(request.FILES['file_upload'])
            post.save()
            return redirect('page_2')
    else:
        form = PostForm()
        return render(request, 'post_create.html', {'form': form})


def Profile_view(request, **kwargs):
    id = kwargs['id']
    user = User.objects.get(id=id)
    def following(request):
        user_follow = Following.objects.get(user=user)
        curr_user = Following.objects.get(user=request.user)
        if request.user not in user_follow.followers.all():
            user_follow.followers.add(request.user)
            user_follow.save()
            curr_user.following.add(user)
            curr_user.save()
        else:
            user_follow.followers.remove(request.user)
            user_follow.save()
            curr_user.following.remove(user)
            curr_user.save()
    following(request)
    user_following = Following.objects.get(user=user)
    return render(request, 'profile_view.html', {'user': user, 'user_following': user_following})


def Profile_editView(request, **kwargs):
    id = kwargs['id']
    user = User.objects.get(id=id)
    print(user)
    if request.method == 'POST':
        form = ProfilForm(request.POST)
        if form.is_valid():
            about = form.cleaned_data['about']
            avatar = form.cleaned_data['avatar']
            profile = Profile(user=user, about=about, avatar=avatar)
            profile.save()
            return redirect('/')
    else:
        form = PostForm()
        return render(request, 'profile_edit.html', {'form': form})


class Search(ListView):
    template_name = 'page_2'
    context_object_name = 'users'


    def get_queryset(self):
        return User.objects.filter(username=self.request.GET.get('q'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context



