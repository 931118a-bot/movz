from django import forms
from .models import Movie, Review


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie  # 사용할 모델
        fields = '__all__'  # MovieForm에서 사용할 Movie 모델의 속성
        exclude = ['create_date', 'modify_date', 'vote']

class ReviewForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 5,
            'maxlength': 300,
            'placeholder': '최대 300자까지 입력 가능합니다.',
            'style': 'resize:none;'
        }),
        max_length=300,  # 서버 검증
        error_messages={'max_length': ''}  # 경고문구 표시하지 않음
    )

    class Meta:
        model = Review
        fields = ['comment']