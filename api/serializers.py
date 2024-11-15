from rest_framework import serializers
from .models import HandbookCategory, HandbookSection, HandbookEntry


# Serializer for read operations (retrieving entries)
class HandbookEntrySerializer(serializers.ModelSerializer):
    section = serializers.CharField(source='section.title', read_only=True)  # Section name

    class Meta:
        model = HandbookEntry
        fields = ['title', 'content', 'image', 'video', 'attachment', 'section', 'section']


# Serializer for create and update operations
class HandbookCreateEntrySerializer(serializers.ModelSerializer):
    section = serializers.SlugRelatedField(slug_field='slug', queryset=HandbookSection.objects.all(), write_only=True)

    class Meta:
        model = HandbookEntry
        fields = ['title', 'content', 'image', 'video', 'attachment', 'section']


class HandbookSectionSerializer(serializers.ModelSerializer):
    entries = HandbookEntrySerializer(many=True, read_only=True)  # Nested entries
    entries_count = serializers.SerializerMethodField()

    class Meta:
        model = HandbookSection
        fields = ['title', 'slug', 'entries', 'entries_count']

    def get_entries_count(self, obj):
        return obj.entries.count()


class HandbookCategorySerializer(serializers.ModelSerializer):
    sections = HandbookSectionSerializer(many=True, read_only=True)  # Nested sections

    class Meta:
        model = HandbookCategory
        fields = ['title', 'slug', 'sections']
