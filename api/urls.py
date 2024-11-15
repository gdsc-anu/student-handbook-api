from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import HandbookCategoryViewSet, HandbookSectionViewSet, HandbookEntryViewSet

router = DefaultRouter()
router.register(r'categories', HandbookCategoryViewSet, basename='handbookcategory')
router.register(r'sections', HandbookSectionViewSet, basename='handbooksection')
router.register(r'entries', HandbookEntryViewSet, basename='handbookentry')

urlpatterns = [
    path('', include(router.urls)),
]
