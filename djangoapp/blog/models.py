from typing import Any
from django.db import models
from django.urls import reverse
from utils.rands import slugfy_new
from django.contrib.auth.models import User
from utils.images import resize_image
from django_summernote.models import AbstractAttachment # type: ignore

class PostAttachment(AbstractAttachment):
    class Meta:
        verbose_name = 'Post Attachment'
        verbose_name_plural = 'Post Attachments'
    
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name
        current_file_name = str(self.file.name)
        super_save = super().save(*args, **kwargs)
        file_changed = False

        if self.file:
            file_changed = current_file_name != self.file.name
        
        if file_changed:
            resize_image(self.file, new_width=900,optimize=True, quality=75)
        
        return super_save
        


class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
    
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True,
        default="",
        blank=True,
        null=True,
        max_length=255
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugfy_new(self.name)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name

class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True,
        default="",
        blank=True,
        null=True,
        max_length=50
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugfy_new(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Page(models.Model):
    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
    
    title = models.CharField(max_length=65)
    slug = models.SlugField(
        unique=True,
        default="",
        blank=True,
        null=True,
        max_length=255
    )
    content = models.TextField()
    is_published = models.BooleanField(
        default=False,
        help_text='Check this box to publish this page.'
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugfy_new(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class PostManager(models.Manager):
    def get_published(self):
        return self.filter(is_published=True).order_by('-pk')
        

class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    objects = PostManager()
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True,
        default="",
        blank=True,
        null=True,
        max_length=255
    )
    excerpt = models.CharField(max_length=150)
    content = models.TextField()
    is_published = models.BooleanField(
        default=True,
        help_text='Check this box to publish this post.'
        )
    
    cover = models.ImageField(
        upload_to='posts/%Y/%m/',
        default='',
        blank=True
    )
    cover_in_post_content = models.BooleanField(
        default=False,
        help_text='Check this box to show the cover image in the post content.'
        )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,blank=True,default=None)
    tags = models.ManyToManyField(Tag, blank=True, default='')

    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='post_created_by'
        )

    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='post_updated_by'
        )

    def get_absolute_url(self):
        if not self.is_published:
            return reverse("blog:index")        
        return reverse('blog:post', args=(self.slug,))
        

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugfy_new(self.title)
        current_cover_name = str(self.cover.name)
        super_save = super().save(*args, **kwargs)
        cover_changed = False

        if self.cover:
            cover_changed = current_cover_name != self.cover.name
        
        if cover_changed:
            resize_image(self.cover, new_width=900,optimize=True, quality=75)
        
        return super_save
        
    def __str__(self):
        return self.title
