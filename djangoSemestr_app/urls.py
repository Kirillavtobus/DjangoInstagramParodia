from django.urls import path
from .import views


urlpatterns = [
    path('', views.home),
    path('page_2/', views.page_2, name='page_2'),
    path('registration/', views.RegistrationView, name='registration'),
    path('login/', views.LoginPage.as_view(), name='login'),
    path('login/accounts/profile/<int:id>', views.ProfileView, name='profile'),
    path('post_create/', views.PostCreateView, name='Post_Create'),
    path('login/accounts/profile/post_create/', views.PostCreateView, name='Post_Create'),
    path('page_2/profile_view/<int:id>', views.UserProfileView.as_view(), name='profile_view'),
    path('post/page_2/profile_view/<int:id>', views.UserProfileView.as_view(), name='profile_view'),
    path('login/accounts/profile/page_2/login/accounts/profile/page_2/login/accounts/profile/page_2/login/accounts/profile/profile_edit/<int:id>', views.Profile_editView, name='profile_edit'),
    path('start_chat/<int:user_id>/', views.StartChatView.as_view(), name='start_chat'),
    path('chats/', views.ChatsView.as_view(), name='chats'),
    path('post/<int:id>/', views.PostView.as_view(), name='post_view')


]