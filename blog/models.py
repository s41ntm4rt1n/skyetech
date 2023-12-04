import math, datetime
from django.utils import timezone, timesince
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import os
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.html import format_html, linebreaks
from django.contrib.auth.models import User
from django.utils.safestring import SafeText

class Post(models.Model):
    title = models.CharField(max_length=255)
    slug =  models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return '/%s/' % self.slug
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Category(models.Model):
    title =  models.CharField(max_length=255)
    slug =  models.SlugField(blank=True, unique=True)

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title 
    
    def get_absolute_url(self):
        return '/%s/' % self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
class Blog(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=999)
    published = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, unique=True)
    post_type = models.ManyToManyField(Post, blank=True)

    class Meta:
        ordering = ('published',)
        verbose_name_plural = 'Blogs'

    def __str__(self):
        return self.title + ' | ' + str(self.author.first_name) + ' ' + str(self.author.last_name)
    @classmethod
    def get_post_type_choices(cls):
        return [(field, field.replace('_', ' ').capitalize()) for field in cls._meta.get_all_field_names() if field.startswith('post_type_')]
    
    def get_absolute_url(self):
        return reverse("blog:post", kwargs={
            'category_slug': self.category.slug,
            'post_slug':self.slug,
        })

    def get_comments_count(self):
        return BlogComment.objects.filter(title=self).count()
    
    def get_tags(self):
        tags = BlogTag.objects.filter(title=self)
        return tags
       # return ", ".join([tag.tag for tag in tags])
    def get_sections(self):
        sections = BlogSection.objects.filter(title=self)
        return sections
    
    def time_to_read(self):
        words = " ".join([section.outline_content for section in self.get_sections()])
        num_words = len(words.split())
        time_in_seconds = num_words
        minutes = math.ceil(time_in_seconds / 60)
        if int(minutes) >= 1:
            return f"{minutes}min read"
        else:
            return f"{minutes} mins read"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

        if self.image:
            image = Image.open(self.image)

            # Resize the image to a desired size
            max_size = (420, 360)
            image.thumbnail(max_size)

            # Prepare the content of the resized image
            img_io = BytesIO()
            image.save(img_io, format='PNG', quality=90)
            img_io.seek(0)
            image_content = ContentFile(img_io.read())

            # Determine the storage backend to use (local storage or Amazon S3)
            if self.image.storage == default_storage:
                # If using local storage, save the resized image back to the same field
                self.image.save(os.path.basename(self.image.name), image_content, save=False)
            else:
                # If using Amazon S3, create a new file with the resized image content and save it
                resized_image_name = f"{os.path.splitext(self.image.name)[0]}_resized.png"
                self.image.storage.save(resized_image_name, image_content)

            super(Blog, self).save(*args, **kwargs)



class BlogTag(models.Model):
    title = models.ForeignKey(Blog, on_delete=models.CASCADE)
    tag = models.CharField(max_length=50)

    def __str__(self):
        return self.tag
    
    def get_absolute_url(self):
       return '/%s/' % self.title
    
class BlogComment(models.Model):
    title = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    commenter_name = models.CharField(max_length=100, blank=True, null=True)
    comment = models.TextField(blank=True, null=False )
    edited = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('edited',)
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.commenter_name

    def time_elapsed(self):
        now = timezone.now()
        elapsed_time = now - self.edited
        days = elapsed_time.days
        hours = elapsed_time.seconds // 3600

        if days > 7:
            return self.edited  # Return the edited time if days are more than 7
        elif days >= 2:
            return f"{days} days ago"
        elif days == 1:
            return f"{days} day ago"
        elif hours >= 1:
            return f"{hours} hours ago"
        else:
            return "Less than an hour ago"
    
class BlogSection(models.Model):
    title = models.ForeignKey(Blog, on_delete=models.CASCADE)
    outline = models.CharField(max_length=1000, blank=True, null=True)
    outline_content = models.TextField()

    def __str__(self):
        return self.outline
    
    def formatted_outline_content(self):
        # Mark the content as safe using SafeText and then format it as HTML using format_html
        return format_html(SafeText(self.outline_content))
    
