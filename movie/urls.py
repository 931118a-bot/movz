from django.urls import path
from . import views

app_name = 'movie'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_id>/', views.detail, name='detail'), # 상세 페이지
    path('create/', views.movie_create, name='movie_create'), # 영화 (상품) 생성
    path('delete/<int:movie_id>/', views.movie_delete, name='movie_delete'), # 영화 (상품) 삭제
    path('modify/<int:movie_id>/', views.movie_modify, name='movie_modify'), # 영화 (상품) 수정
    path('review/create/<int:movie_id>/', views.review_create, name='review_create'), # 리뷰 생성
    path('review/modify/<int:review_id>/', views.review_modify, name='review_modify'), # 리뷰 수정
    path('review/delete/<int:review_id>/', views.review_delete, name='review_delete'), # 리뷰 삭제
    path('vote/<int:movie_id>/', views.vote, name='movie_vote'), # 영화 (상품) 추천
    path('search/', views.search, name='search'),
    path('genre/', views.genre, name='genre')
]
