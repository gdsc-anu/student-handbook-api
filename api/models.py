from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
import itertools



class SlugMixin:
    """
    Mixin to provide reusable logic for generating a unique slug for models that require it.
    """
    slug_field = 'slug'
    slug_from_field = 'name'

    def generate_unique_slug(self):
        original_slug = slugify(getattr(self, self.slug_from_field))
        self.slug = original_slug
        model_class = self.__class__

        for i in itertools.count(1):
            if not model_class.objects.filter(slug=self.slug).exists():
                break
            self.slug = f"{original_slug}-{i}"
        return self.slug


# Function for generating a dynamic path for Cloudinary uploads
def entry_image_folder(instance, filename):
    return f'handbook_entries/{instance.section.category.slug}/{instance.slug}/{filename}'

def entry_attachment_folder(instance, filename):
    return f'handbook_entries/{instance.section.category.slug}/{instance.slug}/attachments/{filename}'


class HandbookCategory(SlugMixin, models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True, db_index=True)
    
    class Meta:
        verbose_name = "Handbook Category"
        verbose_name_plural = "Handbook Categories"
        ordering = ['title']  # Orders categories alphabetically by title.


class HandbookSection(SlugMixin, models.Model):
    category = models.ForeignKey(HandbookCategory, on_delete=models.CASCADE, related_name='sections', db_index=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)


    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Handbook Section"
        verbose_name_plural = "Handbook Sections"
        ordering = ['title']  # Orders sections alphabetically by title.
    
    
class HandbookEntry(SlugMixin, models.Model):
    section = models.ForeignKey(HandbookSection, on_delete=models.CASCADE, related_name='entries', db_index=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True, db_index=True)
    content = models.TextField()
     # Use CloudinaryField for image and file uploads with dynamic paths
    image = CloudinaryField('image', folder=entry_image_folder, blank=True, null=True)
    video = models.URLField(blank=True, null=True)
    attachment = CloudinaryField('file', folder=entry_attachment_folder, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Handbook Entry"
        verbose_name_plural = "Handbook Entries"
        ordering = ['title']  
