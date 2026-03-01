from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Movie(models.Model):
    m_name = models.CharField(max_length=200, default='', verbose_name='영화제목')
    director = models.CharField(max_length=200, default='', verbose_name='감독')
    cast = models.CharField(max_length=200, default='', verbose_name='출연진')
    story = models.TextField(default='', verbose_name='줄거리')
    runtime = models.IntegerField(default='', verbose_name='상영시간')
    m_date = models.IntegerField(default=timezone.now, verbose_name='개봉년도')
    genre1 = models.CharField(max_length=50, default='', verbose_name='장르1')
    m_age = models.CharField(max_length=50, default='', verbose_name='이용등급')
    create_date = models.DateTimeField(default=timezone.now, verbose_name='등록일시')
    modify_date = models.DateTimeField(default=timezone.now, verbose_name='수정일시')
    vote = models.IntegerField(default=0, verbose_name='추천수', blank=True)
    mainphoto = models.ImageField(upload_to='m_img', null=True, blank=True, verbose_name='이미지')
    
    def __str__(self):
        return f"{self.m_name} ({self.m_date})"

class Review(models.Model):
    username = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='작성자')
    m_name = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='영화명')
    comment = models.TextField(default='', verbose_name='리뷰 내용')
    create_date = models.DateTimeField(default=timezone.now, verbose_name='작성일시')
    r_modify = models.BooleanField(default=False, verbose_name='수정 여부')

    def __str__(self):
        return f"{self.m_name.m_name} - {self.comment[:20]}..."