from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'updated', 'timestamp']
    list_display_links = ['updated']
    search_fields = ['title']

    class Meta:
        model = Post


admin.site.register(Post, PostAdmin)
