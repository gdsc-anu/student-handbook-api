from django.urls import path
from . import views

urlpatterns = [
    # URLs for HandbookCategory
    path('categories/', views.handbook, name='category-list-create'),
    #path('categories/<slug:slug>/', views.category_detail, name='category-detail'),
    
    # URLs for HandbookSections within a Category
    path('<slug:category_slug>/sections/', views.section, name='section-list-create'),
    #path('<slug:category_slug>/<slug:section_slug>/', views.section_detail, name='section-detail'),
    
    # URLs for HandbookEntry within a Section of a Category
    path('<slug:category_slug>/<slug:section_slug>/entries/', views.section_entries, name='entry-list-create'),
    path('<slug:category_slug>/<slug:section_slug>/<slug:entry_slug>/', views.entry_detail, name='entry-detail'),
]
