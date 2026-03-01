from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Movie, Review
from .forms import Movie
from .forms import MovieForm, ReviewForm
from django.db.models import Count, Q, F
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
    genres = ['드라마', '코미디', '멜로', '스릴러', '공포', '액션', '판타지']
    top_genre_movies = {}
    for genre in genres:
        genre_movies = Movie.objects.filter(
            genre1__contains=genre
        ).order_by('-vote').first()

        if genre_movies:
            top_genre_movies[genre] = genre_movies
        else:
            top_genre_movies[genre] = None
    context = {
        'top_genre_movies': top_genre_movies
    }
    return render(request, 'movie/index.html', context)


def detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    page = request.GET.get('page', '1')

    review_list = movie.review_set.all().order_by('-create_date')
    paginator = Paginator(review_list, 5)  # 페이지당 5개씩
    page_obj = paginator.get_page(page)

    related_movies = Movie.objects.filter(
        genre1=movie.genre1
    ).exclude(
        id=movie_id 
    ).order_by(
        '-vote' 
    )[:5]
    context = {
        'movie': movie, 
        'review_list': page_obj, 
        'page': page,
        'related_movies': related_movies 
    }
    
    return render(request, 'movie/detail.html', context)

@login_required(login_url='common:login')
def movie_create(request):
    if not request.user.is_superuser:
        messages.error(request, '관리자만 영화 추가가 가능합니다.')
        return redirect('movie:index')

    if request.method == 'POST':
        post_img = request.FILES.get('post_img') # 이미지 업로드 받아오기
        
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid(): # 폼이 유효하다면
            movie = form.save(commit=False) # 임시 저장하여 movie 객체를 리턴받는다.
            movie.create_date = timezone.now() # 실제 저장을 위해 작성일시를 설정한다.
            movie.save() # 데이터를 실제로 저장한다.
            return redirect('movie:index')
    else:
        form = MovieForm()

    context = {'form': form}
    return render(request, 'movie/movie_form.html', context)

def movie_modify(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if not request.user.is_superuser:
        messages.error(request, '수정권한이 없습니다')
        return redirect('movie:detail', movie_id=movie.id)
    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.modify_date = timezone.now()  # 수정일시 저장
            movie.save()
            return redirect('movie:detail', movie_id=movie.id)
    else:
        form = MovieForm(instance=movie)
    context = {'form': form}
    return render(request, 'movie/movie_form.html', context)

def movie_delete(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if not request.user.is_superuser:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('movie:detail', movie_id=movie.id)
    movie.delete()
    return redirect('movie:index')

def review_create(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    
    review_list = movie.review_set.all().order_by('-create_date')
    paginator = Paginator(review_list, 5)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    related_movies = Movie.objects.filter(genre1=movie.genre1).exclude(id=movie.id).order_by('-vote')[:5]

    comment = request.POST.get('comment', '').strip()
    if not comment: 
        context = {'movie': movie, 'review_list': page_obj,  'related_movies': related_movies, 'error_message' : '리뷰 내용을 입력해주세요' }
        return render(request, 'movie/detail.html', context)
    
    if request.method == 'POST':
        movie.review_set.create(username=request.user, comment=request.POST.get('comment'), create_date=timezone.now())
        return redirect('movie:detail', movie_id=movie.id)
    
@login_required(login_url='common:login')
def review_modify(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.user != review.username and not request.user.is_superuser:
        messages.error(request, '수정권한이 없습니다')
        return redirect('movie:detail', movie_id=review.m_name.id)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.modify_date = timezone.now()
            review.r_modify = True
            review.save()
            return redirect('movie:detail', movie_id=review.m_name.id)
    else:
        form = ReviewForm(instance=review)
    context = {'review': review, 'form': form}
    return render(request, 'movie/review_form.html', context)

@login_required(login_url='common:login')
def review_delete(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.user != review.username and not request.user.is_superuser:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('movie:detail', movie_id=review.m_name.id)

    if request.method == "POST":  # 삭제는 POST로만
        review.delete()
        messages.success(request, '리뷰가 삭제되었습니다.')
        return redirect('movie:detail', movie_id=review.m_name.id)

def search(request):
    kw = request.GET.get('kw', '').strip()
    selected_field = request.GET.get('fields', '').strip()
    page = request.GET.get('page', '1')
    sort = request.GET.get('sort', 'popular')  # 검색 기본값

    # 검색어가 없는 경우
    if not kw:
        return render(request, 'movie/search.html', {
            'kw': '',
            'selected_field': selected_field,
            'message': '검색어를 입력해 주세요.',
        })

    # 검색 필드 기본값
    if not selected_field:
        selected_field = 'm_name'

    # 검색 조건
    query_map = {
        'm_name': Q(m_name__icontains=kw),
        'director': Q(director__icontains=kw),
        'cast': Q(cast__icontains=kw),
        'genre1': Q(genre1__icontains=kw),
    }

    # 필터링
    movies = Movie.objects.filter(query_map[selected_field])

    # 정렬 방식
    if sort == 'latest':
        movies = movies.order_by('-m_date')      # 최신순
    elif sort == 'popular':
        movies = movies.order_by('-vote')        # 인기순

    # 검색 결과 없음
    if not movies.exists():
        return render(request, 'movie/search.html', {
            'kw': kw,
            'selected_field': selected_field,
            'message': '검색 결과가 없습니다.',
            'sort': sort,
        })

    # 페이지네이션 (5개씩)
    paginator = Paginator(movies, 5)
    page_obj = paginator.get_page(page)

    # 제목 매핑
    title_map = {
        'm_name': '영화',
        'director': '감독',
        'cast': '출연진',
        'genre1': '장르',
    }

    context = {
        'kw': kw,
        'selected_field': selected_field,
        'movies': page_obj,
        'title': title_map.get(selected_field, '결과'),
        'sort': sort,
    }

    return render(request, 'movie/search.html', context)


@login_required(login_url='common:login')
def vote(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    user = request.user

    if user.is_superuser or user.is_staff:
        messages.warning(request, "관리자는 추천할 수 없습니다.")
        return redirect('movie:detail', movie_id=movie.id)

    movie.vote = F('vote') + 1
    movie.save(update_fields=['vote'])
    movie.refresh_from_db() 

    return redirect('movie:detail', movie_id=movie.id)

def genre(request):

    kw = request.GET.get('kw', '').strip()
    selected_field = request.GET.get('fields', '').strip()
    page = request.GET.get('page', '1')

    if not kw:
        return render(request, 'movie/search.html', {
            'kw': '',
            'selected_field': selected_field,
            'message': '검색어를 입력해 주세요.'
        })

    if not selected_field:
        selected_field = 'm_name'

    query_map = {
        'm_name': Q(m_name__icontains=kw),
        'director': Q(director__icontains=kw),
        'cast': Q(cast__icontains=kw),
        'genre1': Q(genre1__icontains=kw)
    }

    movies = Movie.objects.filter(query_map[selected_field]).order_by('-vote')

    if not movies.exists():
        return render(request, 'movie/search.html', {
            'kw': kw,
            'selected_field': selected_field,
            'message': '검색 결과가 없습니다.'
        })

    paginator = Paginator(movies, 5)
    page_obj = paginator.get_page(page)

    title_map = {
        'm_name': '영화',
        'director': '감독',
        'cast': '출연진',
        'genre1': '장르'
    }

    context = {
        'kw': kw,
        'selected_field': selected_field,
        'movies': page_obj,
        'title': title_map.get(selected_field, '결과'),
    }
    return render(request, 'movie/genre.html', context)