from django.contrib import admin
from .models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'nick', 'gender', 'city', 'skill', 'contacts', 'private')
    list_display_links = ('id', 'nick', 'city',)
    search_fields = ('nick', 'city', 'skill', 'contacts', )
    list_filter = ('gender', 'city', 'skill', 'private', )


class SnapshotAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'description', 'categories', 'camera', 'city', 'region', 'country', 'timestamp')
    list_display_links = ('id', 'description', )
    search_fields = ('author', 'camera', 'category',)
    list_filter = ('author', 'camera', 'category', )


class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'person_in_snap')
    list_display_links = ('id', 'name',)
    search_fields = ('name',)
    list_filter = ('name',)


class CameraAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand')
    list_display_links = ('id', 'brand',)
    search_fields = ('brand',)
    list_filter = ('brand',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'author', 'text', 'post_id')
    list_display_links = ('author',)
    search_fields = ('author',)
    list_filter = ('author',)


class SubListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    list_display_links = ('user',)
    search_fields = ('user',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'snap_count')
    list_display_links = ('name',)
    search_fields = ('name',)


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Snapshot, SnapshotAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Camera, CameraAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(SubList, SubListAdmin)
admin.site.register(Category, CategoryAdmin)
