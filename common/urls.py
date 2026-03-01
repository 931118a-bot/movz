from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'common'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(template_name='common/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('usercheck/', views.usercheck, name='usercheck'),
    path('userinfo/', views.userinfo, name='userinfo'),
    path('user_modify/', views.user_modify, name='user_modify'),
]