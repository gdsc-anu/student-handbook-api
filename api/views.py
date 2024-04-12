from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import HandbookCategory, HandbookSection, HandbookEntry
from .serializers import HandbookCategorySerializer, HandbookSectionSerializer, HandbookEntrySerializer

@api_view(['GET'])
def handbook(request):
    if request.method == 'GET':
        categories = HandbookCategory.objects.all()
        serializer = HandbookCategorySerializer(categories, many=True)
        return Response(serializer.data)

"""
    elif request.method == 'POST':
        serializer = HandbookCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
"""
    
"""	

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, slug):
    try:
        category = HandbookCategory.objects.get(slug=slug)
    except HandbookCategory.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = HandbookCategorySerializer(category)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = HandbookCategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return Response({'detail': 'Handbook Category deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

"""

@api_view(['GET'])
def section(request, category_slug):
    try:
        category = HandbookCategory.objects.get(slug=category_slug)
    except HandbookCategory.DoesNotExist:
        return Response({'detail': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        sections = HandbookSection.objects.filter(category=category)
        serializer = HandbookSectionSerializer(sections, many=True)
        return Response(serializer.data)
    
"""
    elif request.method == 'POST':
        request.data['category'] = category.id  # Attach category ID to the section data
        serializer = HandbookSectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
"""

"""

@api_view(['GET', 'PUT', 'DELETE'])
def section_detail(request, category_slug, section_slug):
    try:
        category = HandbookCategory.objects.get(slug=category_slug)
        section = HandbookSection.objects.get(category=category, slug=section_slug)
    except (HandbookCategory.DoesNotExist, HandbookSection.DoesNotExist):
        return Response({'detail': 'Category or Section not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = HandbookSectionSerializer(section)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = HandbookSectionSerializer(section, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        section.delete()
        return Response({'detail': 'Handbook Section deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

"""
    
@api_view(['GET'])
def section_entries(request, category_slug, section_slug):
    try:
        category = HandbookCategory.objects.get(slug=category_slug)
        section = HandbookSection.objects.get(category=category, slug=section_slug)
    except HandbookCategory.DoesNotExist or HandbookSection.DoesNotExist:
        return Response({'detail': 'Category or Section not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        entries = HandbookEntry.objects.filter(section=section)
        serializer = HandbookEntrySerializer(entries, many=True)
        return Response(serializer.data)

"""

    elif request.method == 'POST':
        request.data['section'] = section.id  # Attach section ID to the entry data
        serializer = HandbookEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
""" 
    
@api_view(['GET'])
def entry_detail(request, category_slug, section_slug, entry_slug):
    try:
        # Ensure the category exists
        category = HandbookCategory.objects.get(slug=category_slug)
        # Ensure the section exists within the given category
        section = HandbookSection.objects.get(category=category, slug=section_slug)
        # Finally, get the entry within the specified section
        entry = HandbookEntry.objects.get(section=section, slug=entry_slug)
    except (HandbookCategory.DoesNotExist, HandbookSection.DoesNotExist, HandbookEntry.DoesNotExist):
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = HandbookEntrySerializer(entry)
        return Response(serializer.data)
    
    """
    elif request.method == 'PUT':
        serializer = HandbookEntrySerializer(entry, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    """

    