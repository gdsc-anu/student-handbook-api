from rest_framework import serializers
from .models import HandbookCategory, HandbookSection, HandbookEntry


# Serializer for read operations (retrieving entries)
class HandbookEntrySerializer(serializers.ModelSerializer):
    # section = serializers.CharField(source='section.title', read_only=True)  # Section name

    class Meta:
        model = HandbookEntry
        fields = ['id', 'title', 'slug', 'content', 'image', 'video', 'attachment']


# Serializer for create and update operations
class HandbookCreateEntrySerializer(serializers.ModelSerializer):
    section = serializers.SlugRelatedField(slug_field='slug', queryset=HandbookSection.objects.all(), write_only=True)

    class Meta:
        model = HandbookEntry
        fields = ['title', 'content', 'image', 'video', 'attachment', 'section']


class HandbookSectionSerializer(serializers.ModelSerializer):
    entries_count = serializers.SerializerMethodField()
    entries = HandbookEntrySerializer(many=True, read_only=True)  # Nested entries

    class Meta:
        model = HandbookSection
        fields = ['id', 'title', 'slug', 'entries_count', 'entries']

    def get_entries_count(self, obj):
        return obj.entries.count()


class HandbookCategorySerializer(serializers.ModelSerializer):
    sections_count = serializers.SerializerMethodField()
    sections = HandbookSectionSerializer(many=True, read_only=True)  # Nested sections


    class Meta:
        model = HandbookCategory
        fields = ['id', 'title', 'slug', 'sections_count', 'sections']

    def get_sections_count(self, obj):
        return obj.sections.count()
