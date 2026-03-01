from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import transaction 
from .models import Profile, User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .forms import UserModifyForm, UserForm
from django.conf import settings
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.views import LoginView
from django.urls import reverse
from urllib.parse import urlencode
import json

class CustomLoginView(LoginView):
    success_url = '/'
    def form_invalid(self, form):
        messages.error(self.request, "사용자 ID 또는 비밀번호가 올바르지 않습니다.")
        next_url = self.request.POST.get('next') or self.request.GET.get('next')
        login_path = reverse("common:login")
        if next_url:
            query_params = {'next': next_url}
            encoded_params = urlencode(query_params)
            return redirect(f'{login_path}?{encoded_params}')
        return redirect(login_path)
    
def logout_view(request):
    logout(request)
    next_url = request.GET.get('next') 
    if next_url and url_has_allowed_host_and_scheme(
        url=next_url, 
        allowed_hosts={request.get_host()},  
        require_https=request.is_secure()    
    ):
        redirect_to = next_url
        return redirect(redirect_to)

    return redirect('index')

def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                Profile.objects.create(
                    user=user,
                    name=form.cleaned_data.get('name'),
                    phone=form.cleaned_data.get('phone')
                )  
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                if user is not None:
                    login(request, user)  
                    return redirect('index')
                return redirect('common:login')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})



@login_required
def usercheck(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('index')
    if request.method == 'POST':
        password = request.POST.get('password')
        username = request.user.username
        user = authenticate(request, username=username, password=password)
        if user is not None:
            current_user = request.user 
            try:
                with transaction.atomic():
                    if hasattr(current_user, 'profile'):
                        current_user.profile.delete()
                    current_user.delete()
                logout(request)
                return redirect('index')

            except Exception as e:
                messages.error(request, "회원 탈퇴 중 오류가 발생했습니다. 다시 시도해 주세요.")
                return redirect('common:usercheck') 
        else:
            messages.error(request, "비밀번호가 일치하지 않습니다.")
    return render(request, 'common/usercheck.html')

@login_required
def userinfo(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('index')
    current_user = request.user
    try:
        user_profile = current_user.profile
    except Profile.DoesNotExist:
        user_profile = None
    context = {
        'user': current_user,
        'profile': user_profile,
    }
    return render(request, 'common/userinfo.html', context)

@login_required
def user_modify(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('index')
    current_user = request.user
    
    try:
        user_profile = current_user.profile
    except Profile.DoesNotExist:
        messages.error(request, "프로필 정보가 없습니다. 회원가입을 다시 시도해주세요.")
        return redirect('common:userinfo')

    if request.method == 'POST':
        form = UserModifyForm(request.POST)
        if form.is_valid():
            
            with transaction.atomic():
                current_user.email = form.cleaned_data['email']
                new_password1 = form.cleaned_data.get('new_password1')
                if new_password1:
                    current_user.password = make_password(new_password1)
                
                current_user.save()

                user_profile.name = form.cleaned_data['name']
                user_profile.phone = form.cleaned_data['phone']
                user_profile.save()
                if isinstance(current_user, User):
                    login(request, current_user)
            
            messages.success(request, "정보가 성공적으로 수정되었습니다.")
            return redirect('common:userinfo')
    else:
        initial_data = {
            'email': current_user.email,
            'name': user_profile.name,
            'phone': user_profile.phone,
        }
        form = UserModifyForm(initial=initial_data)

    context = {'form': form}
    return render(request, 'common/user_modify.html', context)