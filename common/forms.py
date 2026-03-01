from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    name = forms.CharField(label="이름", max_length=50)
    phone = forms.CharField(label="전화번호", max_length=20)
    
    class Meta:
        model = User
        fields = ( "name", "username", "password1", "password2", "email", "phone")


numeric_validator = RegexValidator(r'^\d+$', '전화번호는 - 없이 숫자만 입력해야 합니다.')

class UserModifyForm(forms.Form):
    email = forms.EmailField(label="이메일", max_length=254)
    name = forms.CharField(label="이름", max_length=50)
    phone = forms.CharField(label="전화번호", max_length=20, validators=[numeric_validator])
    new_password1 = forms.CharField(label="새 비밀번호", widget=forms.PasswordInput, required=False)
    new_password2 = forms.CharField(label="새 비밀번호 확인", widget=forms.PasswordInput, required=False)
    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")
        if new_password1 and new_password2 and new_password1 != new_password2:
            self.add_error('new_password2', "새 비밀번호가 일치하지 않습니다.")
        return cleaned_data