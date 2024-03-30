from django.db import models
from django.utils.text import slugify

class HandbookCategory(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(HandbookCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Handbook Category"
        verbose_name_plural = "Handbook Categories"
        ordering = ['title']  # Orders categories alphabetically by title.

class HandbookSection(models.Model):
    category = models.ForeignKey(HandbookCategory, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(HandbookSection, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Handbook Section"
        verbose_name_plural = "Handbook Sections"
        unique_together = ('title', 'slug')
        ordering = ['title']  # Orders sections alphabetically by title.
    
class HandbookEntry(models.Model):
    section = models.ForeignKey(HandbookSection, on_delete=models.CASCADE, related_name='entries')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='content_images', blank=True, null=True)
    video = models.URLField(blank=True, null=True)
    attachment = models.FileField(upload_to='content_attachments', blank=True, null=True) # Changed the upload_to path for clarity

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(HandbookEntry, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Handbook Entry"
        verbose_name_plural = "Handbook Entries"
        unique_together = ('title', 'slug') 
        ordering = ['title']  
