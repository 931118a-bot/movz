from django.contrib import admin
from .models import Movie, Review

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    
    search_fields = ['m_name', 'director', 'cast', 'genre1']

    exclude = ('vote',)