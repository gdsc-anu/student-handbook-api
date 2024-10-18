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
    list_display = ('title', 'slug', 'section_count')  # Display count of sections
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)
    ordering = ('title',)
    inlines = [HandbookSectionInline]

    # Adding method to display section count in the admin list view
    def section_count(self, obj):
        return obj.sections.count()
    section_count.short_description = 'Number of Sections'


@admin.register(HandbookSection)
class HandbookSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'slug', 'entry_count')  # Display count of entries
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'category__title')
    ordering = ('category', 'title')
    list_filter = ('category',)
    inlines = [HandbookEntryInline]
    autocomplete_fields = ['category']  # Enables autocomplete for categories

    # Adding method to display entry count in the admin list view
    def entry_count(self, obj):
        return obj.entries.count()
    entry_count.short_description = 'Number of Entries'


@admin.register(HandbookEntry)
class HandbookEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'section__title')
    ordering = ('section', 'title')
    list_filter = ('section', 'section__category')  # Simplified list filter
    autocomplete_fields = ['section']  # Enables autocomplete for sections
    readonly_fields = ('slug',)  # Make slug read-only in the admin interface
