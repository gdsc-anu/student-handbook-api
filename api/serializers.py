from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from .models import HandbookCategory, HandbookSection, HandbookEntry

class HandbookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HandbookCategory
        fields = ['id', 'title', 'slug']

class HandbookSectionSerializer(serializers.ModelSerializer):
    entries_count = serializers.SerializerMethodField()

    class Meta:
        model = HandbookSection
        fields = ['id', 'category', 'title', 'slug', 'entries_count']
    
    def get_entries_count(self, obj):
        return obj.entries.count()

class HandbookEntrySerializer(serializers.ModelSerializer):
    section_slug = serializers.SlugField(write_only=True)  # Add this field

    class Meta:
        model = HandbookEntry
        fields = ['id', 'section', 'title', 'slug', 'content', 'image', 'video', 'attachment', 'section_slug']  # Include 'section_slug' in fields

    def create(self, validated_data):
        section_slug = validated_data.pop('section_slug')
        try:
            section = HandbookSection.objects.get(slug=section_slug)
        except HandbookSection.DoesNotExist:
            raise ValidationError({'section_slug': 'No section found with this slug.'})
        validated_data['section'] = section
        entry = HandbookEntry.objects.create(**validated_data)
        return entry

    def update(self, instance, validated_data):
        section_slug = validated_data.pop('section_slug', None)
        if section_slug:
            section = HandbookSection.objects.get(slug=section_slug)
            instance.section = section

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance