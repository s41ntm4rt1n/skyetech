from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.html import format_html
from django.utils.safestring import SafeText


class Member(models.Model):
    name=models.CharField(max_length=255)
    reg_no=models.CharField(max_length=20)
    role=models.CharField(max_length=255, blank=True, null=True)
    image=models.ImageField(upload_to='team/', blank=True, null=True)
    about=models.TextField(blank=True)
    phone=models.CharField(max_length=13, blank=True)
    email=models.EmailField(max_length=255, blank=True)
    slug=models.SlugField(unique=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def get_urls(self):
        urls=Url.objects.filter(member_name=self)
        return urls
    
    def get_absolute_url(self):
        return reverse('team_details', kwargs={
            'slug': self.slug})
        
class About(models.Model):
    about=models.TextField()
    mission=models.TextField()
    vision=models.TextField()
    
    def __str__(self):
        return f'About Us'
    
    
class Project(models.Model):
    title=models.CharField(max_length=225)
    category=models.CharField(max_length=225, blank=True)
    description=models.TextField(blank=True)
    image=models.ImageField(upload_to='projects/', blank=True, null=True)
    slug=models.SlugField(unique=True, blank=True)
    url=models.URLField(blank=True)
    client=models.CharField(max_length=225, blank=True)
    updated=models.DateField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('project', kwargs={
            'slug': self.slug})
        
    def get_documentation_absolute_url(self):
        return reverse('documentation', kwargs={
            'slug': self.slug})
        

class Part(models.Model):
    project=models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    title=models.CharField(max_length=225)
    description=models.TextField(blank=True)
    url=models.URLField(blank=True)
    
    def __str__(self):
        return self.title
    
class Url(models.Model):
    member_name=models.ForeignKey(Member, on_delete=models.CASCADE)
    title=models.CharField(max_length=225)
    url=models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.title
    
class Services(models.Model):
    name=models.CharField(max_length=225)
    description=models.TextField(blank=True)
    image=models.ImageField(upload_to='services/', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'Services'
        
    def __str__(self):
        return self.name
    
class Contact(models.Model):
    address=models.CharField(max_length=225)
    email=models.CharField(max_length=225)
    phone=models.CharField(max_length=225)
    
    def __str__(self):
        return f'Contact Info'