from django.contrib import admin
from .models import HandbookCategory, HandbookSection, HandbookEntry

class HandbookSectionInline(admin.TabularInline):
    model = HandbookSection
    extra = 1  # Number of extra forms to display
    prepopulated_fields = {'slug': ('title',)}

class HandbookEntryInline(admin.TabularInline):
    model = HandbookEntry
    extra = 1
    prepopulated_fields = {'slug': ('title',)}

@admin.register(HandbookCategory)
class HandbookCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)
    ordering = ('title',)
    inlines = [HandbookSectionInline]

@admin.register(HandbookSection)
class HandbookSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'category__title')
    ordering = ('category', 'title')
    list_filter = ('category',)
    inlines = [HandbookEntryInline]

@admin.register(HandbookEntry)
class HandbookEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'section__title')
    ordering = ('section', 'title')
    list_filter = ('section', 'section__category', 'section__category__title')