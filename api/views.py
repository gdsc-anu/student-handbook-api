from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import HandbookCategory, HandbookSection, HandbookEntry
from .serializers import (
    HandbookCategorySerializer, 
    HandbookSectionSerializer, 
    HandbookEntrySerializer, 
    HandbookCreateEntrySerializer
)

# ViewSet for HandbookCategory
class HandbookCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Handbook Categories. Supports:
    - Listing all categories
    - Retrieving a single category
    - Creating a new category
    - Updating an existing category
    - Deleting a category
    - Retrieving all sections under a category
    """
    
    queryset = HandbookCategory.objects.all()
    serializer_class = HandbookCategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['id', 'title']  # Enables search on 'title' field
    ordering_fields = ['id', 'title']  # Enables ordering by 'title'
    orderiing = ['id']

    @swagger_auto_schema(
        operation_description="Create a new handbook category",
        request_body=HandbookCategorySerializer,
        responses={201: HandbookCategorySerializer, 400: 'Validation Error'}
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new handbook category.
        
        - `title`: Title of the category.
        - Returns the created category with a slug.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Update an existing handbook category",
        request_body=HandbookCategorySerializer,
        responses={200: HandbookCategorySerializer, 400: 'Validation Error'}
    )
    def update(self, request, *args, **kwargs):
        """
        Update an existing handbook category.
        
        - `title`: Updated title of the category.
        - Returns the updated category with the new details.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Delete a handbook category",
        responses={204: 'No Content', 404: 'Not Found'}
    )
    def destroy(self, request, *args, **kwargs):
        """
        Delete an existing handbook category.
        
        - Deletes the specified category from the database.
        - Returns `204 No Content` on successful deletion.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_description="Retrieve sections for a specific handbook category",
        responses={200: HandbookSectionSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def sections(self, request, pk=None):
        """
        Retrieve all sections for a specific handbook category.
        
        - Returns a list of sections under the specified category.
        """
        category = self.get_object()
        sections = category.sections.all()
        serializer = HandbookSectionSerializer(sections, many=True)
        return Response(serializer.data)
    
    

# ViewSet for HandbookSection
class HandbookSectionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Handbook Sections. Supports:
    - Listing all sections
    - Retrieving a single section
    - Creating a new section
    - Updating an existing section
    - Deleting a section
    - Retrieving all entries under a section
    """
    
    queryset = HandbookSection.objects.all()
    serializer_class = HandbookSectionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category']  # Enables filtering by 'category'
    search_fields = ['title', 'category__title']  # Enables search on 'title' and 'category title'
    ordering_fields = ['id', 'title', 'category__title']  # Enables ordering by 'title' and 'category title'
    orderiing = ['id']


    @swagger_auto_schema(
        operation_description="Create a new handbook section",
        request_body=HandbookSectionSerializer,
        responses={201: HandbookSectionSerializer, 400: 'Validation Error'}
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new handbook section.
        
        - `title`: Title of the section.
        - `category`: The category to which the section belongs.
        - Returns the created section with a slug.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Update an existing handbook section",
        request_body=HandbookSectionSerializer,
        responses={200: HandbookSectionSerializer, 400: 'Validation Error'}
    )
    def update(self, request, *args, **kwargs):
        """
        Update an existing handbook section.
        
        - `title`: Updated title of the section.
        - `category`: Updated category to which the section belongs.
        - Returns the updated section with new details.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Delete a handbook section",
        responses={204: 'No Content', 404: 'Not Found'}
    )
    def destroy(self, request, *args, **kwargs):
        """
        Delete an existing handbook section.
        
        - Deletes the specified section from the database.
        - Returns `204 No Content` on successful deletion.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_description="Retrieve entries for a specific handbook section",
        responses={200: HandbookEntrySerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def entries(self, request, pk=None):
        """
        Retrieve all entries for a specific handbook section.
        
        - Returns a list of entries under the specified section.
        """
        section = self.get_object()
        entries = section.entries.all()
        serializer = HandbookEntrySerializer(entries, many=True)
        return Response(serializer.data)


# ViewSet for HandbookEntry
class HandbookEntryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Handbook Entries. Supports:
    - Listing all entries
    - Retrieving a single entry
    - Creating a new entry
    - Updating an existing entry
    - Deleting an entry
    """

    queryset = HandbookEntry.objects.all()

    # Use different serializers for read and write operations
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return HandbookCreateEntrySerializer
        return HandbookEntrySerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['section']  # Enables filtering by 'section'
    search_fields = ['title', 'section__title', 'section__category__title']  # Search on 'title', 'section', and 'category title'
    ordering_fields = ['id', 'title', 'section__title', 'section__category__title']  # Ordering by title, section title, and category title
    ordering = ['id']
    
    @swagger_auto_schema(
        operation_description="Create a new handbook entry",
        request_body=HandbookCreateEntrySerializer,
        responses={201: HandbookEntrySerializer, 400: 'Validation Error'}
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new handbook entry.
        
        - `title`: Title of the entry.
        - `content`: The content of the entry.
        - `image`: Optional image for the entry.
        - `video`: Optional video URL for the entry.
        - `attachment`: Optional file attachment for the entry.
        - `section_slug`: The slug of the section to which the entry belongs.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Update an existing handbook entry",
        request_body=HandbookCreateEntrySerializer,
        responses={200: HandbookEntrySerializer, 400: 'Validation Error'}
    )
    def update(self, request, *args, **kwargs):
        """
        Update an existing handbook entry.
        
        - `title`: Updated title of the entry.
        - `content`: Updated content of the entry.
        - `image`: Updated image for the entry.
        - `video`: Updated video URL for the entry.
        - `attachment`: Updated file attachment for the entry.
        - `section_slug`: The slug of the section to which the entry belongs.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Delete a handbook entry",
        responses={204: 'No Content', 404: 'Not Found'}
    )
    def destroy(self, request, *args, **kwargs):
        """
        Delete an existing handbook entry.
        
        - Deletes the specified entry from the database.
        - Returns `204 No Content` on successful deletion.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
