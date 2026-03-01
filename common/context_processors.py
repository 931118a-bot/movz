from django.conf import settings

def previous_url_processor(request):
    # 'Referer' 헤더에서 이전 URL을 가져옵니다.
    # 안전하지 않은 URL이나, Referer가 없는 경우(직접 입력, 새 탭 등)를 대비합니다.
    referer_url = request.META.get('HTTP_REFERER')
    
    # 기본값 설정 (설정된 HOME_URL 또는 루트 경로 '/')
    default_url = getattr(settings, 'HOME_URL', '/')
    
    previous_url = default_url
    
    # 1. Referer가 있고, 현재 페이지와 다를 경우에만 사용
    if referer_url and referer_url != request.build_absolute_uri():
        previous_url = referer_url
        
    # 2. Referer가 현재 페이지의 URL을 포함하는 경우 (같은 페이지 내 앵커 이동 등)도 방지
    # URL을 정규화하여 비교하는 것이 더 안전하지만, 단순하게 문자열 비교로 처리합니다.
    if request.get_full_path() in previous_url:
        previous_url = default_url

    return {'previous_url': previous_url}