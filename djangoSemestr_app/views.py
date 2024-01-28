from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from .forms import RegistrationForm, LoginForm, PostForm, ProfilForm, ChatForm, CommentForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from .models import Post, Following, Profile, Chat, Message, Comment
from django.views.generic.base import TemplateView, RedirectView
from django.utils.translation import gettext as _


def home(request):
    users = User.objects.all()
    user = request.user
    posts = Post.objects.all()
    user_following = Following.objects.get(user=user)
    following = user_following.following
    return render(request, 'home.html', {'posts': posts, 'user': user})


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
            user_profile = Profile(user=user_foll)
            user_profile.save()
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
    profile = Profile.objects.get(user=user)
    f_user = Following.objects.get(user=user)
    followers = len(f_user.followers.all())
    following = len(f_user.following.all())
    return render(request, 'profile.html', {'user': user, 'foll': foll, 'profile': profile, 'followers': followers, 'following': following})


def handle_upload_file(f):
    with open(f'djangoSemestr_app/static/{f.name}', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


class PostView(CreateView):
    template_name = 'post.html'
    form_class = CommentForm


    def post(self, request, *args, **kwargs):
        post_data = request.POST
        post = Post.objects.get(id=self.kwargs['id'])
        user = self.request.user
        if 'comment' in post_data.keys():
            comment = Comment(comment=post_data['comment'], user=user, post=post)
            comment.save()
            resp = render_to_string('comment.html', {'i': comment})
            return JsonResponse(resp, safe=False)

        if 'delete_comment' in post_data.keys():
            comment = Comment.objects.get(id=int(post_data['delete_comment']))
            comment_id = comment.id
            comment.delete()
            data = {'id': comment_id}
            return JsonResponse(data, safe=False)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(id=self.kwargs['id'])
        context['post'] = Post.objects.get(id=self.kwargs['id'])
        context['form'] = CommentForm()
        context['comments'] = Comment.objects.filter(post=post)
        return context


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


class UserProfileView(TemplateView):
    template_name = 'profile_view.html'

    def post(self, request, **kwargs):
        data_post = request.POST
        current_user = self.request.user
        current_user_follow = Following.objects.get(user=current_user)
        f_user = Following.objects.get(user=User.objects.get(id=data_post['follow']))
        if data_post['is_followed'] == '0':
            current_user_follow.following.add(User.objects.get(id=data_post['follow']))
            current_user_follow.save()
            f_user.followers.add(current_user)
            f_user.save()
            return JsonResponse({'is_follow': 1, 'followers': len(f_user.followers.all())})
        else:
            current_user_follow.following.remove(User.objects.get(id=data_post['follow']))
            current_user_follow.save()
            f_user.followers.remove(current_user)
            f_user.save()
            return JsonResponse({'is_follow': 0, 'followers': len(f_user.followers.all())})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        current_user_follow = Following.objects.get(user=current_user)
        user = User.objects.get(id=kwargs['id'])
        context['is_followed'] = 1
        if user not in current_user_follow.following.all():
            context['is_followed'] = 0
        context['title'] = user.username
        context['followers'] = len(current_user_follow.followers.all())
        context['following'] = len(current_user_follow.following.all())
        context['current_user'] = current_user
        context['user'] = user
        context['posts'] = Post.objects.filter(user=user)
        context['post_am'] = len(Post.objects.filter(user=user))
        return context


class StartChatView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        user1 = User.objects.get(id=self.kwargs['user_id'])
        for c in Chat.objects.all():
            if user in c.members.all() and user1 in c.members.all():
                self.url = '/chats'
                break
        else:
            chat = Chat()
            chat.save()
            chat.members.add(user, user1)
            self.url = '/chats'
        return super().get_redirect_url(*args, **kwargs)


class ChatsView(TemplateView):
    template_name = 'chats.html'

    def post(self, request):
        data_post = request.POST
        user = self.request.user
        chat = Chat.objects.get(id=data_post['chat'])
        if 'message' in data_post.keys():
            message = Message(user=user, chat=chat, body=data_post['message'])
            message.save()
            return JsonResponse({'message': message.body}, safe=False)
        messages = Message.objects.filter(chat=chat)
        form = ChatForm()
        result = render_to_string('chat.html', {'messages': messages, 'form': form, 'chat': chat, 'user': user})
        return JsonResponse(result, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        chats = []
        for c in Chat.objects.all():
            if user in c.members.all():
                for u in c.members.all():
                    if u != user:
                        chats.append([c, u])
        context['profile'] = user
        context['chats'] = chats
        context['title'] = _('Chat')
        return context


__all__ = ['ChatsView', 'StartChatView']


def Profile_editView(request, **kwargs):
    id = kwargs['id']
    user = User.objects.get(id=id)
    profile_user = Profile.objects.get(user=user)
    if request.method == 'POST':
        form = ProfilForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            about = form.cleaned_data['about']
            avatar = form.cleaned_data['avatar']
            profile_user.avatar = avatar
            profile_user.save()
            profile_user.about = about
            profile_user.save()
            return redirect('/')
    else:
        form = PostForm()
    return render(request, 'profile_edit.html', {'form': form})



