def show_search_context(request):
    path = request.path

    # 검색창을 숨길 경로들
    hide_paths = [
        '/common',     
        '/movie/create', 
        '/movie/modify',    
        '/movie/review/modify',   
    ]

    # hide_paths 중 하나로 시작하면 show_search = False
    show_search = not any(path.startswith(p) for p in hide_paths)

    return {'show_search': show_search}