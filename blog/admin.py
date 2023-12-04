from django.contrib import admin
from .models import *

admin.site.register(Post)

class BlogTagInline(admin.StackedInline):
    model = BlogTag
    extra = 1

class BlogSectionInLine(admin.StackedInline):
    model = BlogSection
    extra = 1

class BlogCommentInLine(admin.StackedInline):
    model = BlogComment
    extra = 1

class BlogAdmin(admin.ModelAdmin):
    filter_horizontal = ('post_type',)
    search_fields = ['title', 'category', 'outline', 'outline_content']
    list_display=['title','category','published']
    list_filter = ['category', 'published']
    prepopulated_fields = {'slug': ('title',)}
    inlines = (BlogTagInline, BlogSectionInLine,BlogCommentInLine,)
admin.site.register(Blog, BlogAdmin)

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Category)

