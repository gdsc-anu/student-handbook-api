from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
import itertools


class SlugMixin:
    """
    Mixin to provide reusable logic for generating a unique slug for models that require it.
    """
    slug_field = 'slug'  # Field where the slug will be stored
    slug_from_field = 'title'  # Field from which the slug will be generated
    
    def save(self, *args, **kwargs):
        # Generate slug only if it's not already set
        if not getattr(self, self.slug_field):
            self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        original_slug = slugify(getattr(self, self.slug_from_field))
        slug = original_slug
        model_class = self.__class__

        # Ensure slug is unique within the model
        for i in itertools.count(1):
            if not model_class.objects.filter(**{self.slug_field: slug}).exists():
                break
            slug = f"{original_slug}-{i}"

        setattr(self, self.slug_field, slug)
        return slug


# # Function for generating a dynamic path for Cloudinary uploads
# def entry_image_folder(instance, filename=None):
#     if not instance.slug:
#         instance.generate_unique_slug()
#     return f'handbook_entries/{instance.section.category.slug}/{instance.slug}/{filename or "default_image.jpg"}'

# def entry_attachment_folder(instance, filename=None):
#     if not instance.slug:
#         instance.generate_unique_slug()
#     return f'handbook_entries/{instance.section.category.slug}/{instance.slug}/attachments/{filename or "default_file.txt"}'



class HandbookCategory(SlugMixin, models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True, db_index=True)
    
    class Meta:
        verbose_name = "Handbook Category"
        verbose_name_plural = "Handbook Categories"
        ordering = ['title']

    def __str__(self):
        return self.title


class HandbookSection(SlugMixin, models.Model):
    category = models.ForeignKey(HandbookCategory, on_delete=models.CASCADE, related_name='sections', db_index=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    class Meta:
        verbose_name = "Handbook Section"
        verbose_name_plural = "Handbook Sections"
        ordering = ['title']

    def __str__(self):
        return self.title


class HandbookEntry(SlugMixin, models.Model):
    section = models.ForeignKey(HandbookSection, on_delete=models.CASCADE, related_name='entries', db_index=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True, db_index=True)
    content = models.TextField()
    # Use CloudinaryField for image and file uploads with dynamic paths
    image = CloudinaryField(
        'image',
        blank=True,
        null=True,
        resource_type='image',
        folder='Handbook Images',
        unique_filename=True
    )
    video = models.URLField(blank=True, null=True)
    attachment = CloudinaryField(
        'file',
        blank=True,
        null=True,
        resource_type='raw',
        folder='Handbook Files',
        unique_filename=True
    )

    class Meta:
        verbose_name = "Handbook Entry"
        verbose_name_plural = "Handbook Entries"
        ordering = ['title']

    def __str__(self):
        return self.title
