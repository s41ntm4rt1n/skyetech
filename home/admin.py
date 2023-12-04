from django.contrib import admin
from .models import *

admin.site.register(Project)
admin.site.register(About)
admin.site.register(Part)
admin.site.register(Services)
class UrlInLine(admin.StackedInline):
    model=Url
    extra = 1

class MemberAdmin(admin.ModelAdmin):
    model = Member
    inlines = (UrlInLine,)
    prepopulated_fields= {'slug': ('name',)}
    
admin.site.register(Member, MemberAdmin)
