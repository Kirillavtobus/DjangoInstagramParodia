from django.urls import path
from .import views
from .views import Search

urlpatterns = [
    path('', views.home),
    path('page_2/', views.page_2, name='page_2'),
    path('registration/', views.RegistrationView, name='registration'),
    path('login/', views.LoginPage.as_view(), name='login'),
    path('page_2/login/accounts/profile/<int:id>', views.ProfileView, name='profile'),
    path('post_create/', views.PostCreateView, name='Post_Create'),
    path('page_2/profile_view/<int:id>', views.Profile_view, name='profile_view'),
    path('page_2/login/accounts/profile/page_2/login/accounts/profile/page_2/login/accounts/profile/page_2/login/accounts/profile/profile_edit/<int:id>', views.Profile_editView, name='profile_edit'),
    path('search/?q=', views.Search.as_view(), name='search')

]