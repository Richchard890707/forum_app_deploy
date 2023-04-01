from unicodedata import category
from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django_resized import ResizedImageField
from tinymce.models import HTMLField
from tinymce import models as tinymce_models
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from taggit.managers import TaggableManager
from django.shortcuts import reverse
import uuid

User = get_user_model()

class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=40, blank=True)
    slug = slug = models.SlugField(max_length=400, unique=True, blank=True)
    bio = tinymce_models.HTMLField()
    points = models.IntegerField(default=0)
    profile_pic = ResizedImageField(size=[50, 80], quality=100, upload_to="authors", default=None, null=True, blank=True)

    def __str__(self):
        return self.fullname

    @property #調用成員變量而不是函數一樣調用它
    def num_posts(self):
        return Post.objects.filter(user=self).count()

    #automatically save the slug
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.fullname)
        super(Author, self).save(*args, **kwargs)

class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    description = models.TextField(default="description")
    #change the metadata of the model
    class Meta:
        #change the plural version name of the model
        verbose_name_plural = "categories"
    #did with other model
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)
    #change detail to post
    def get_url(self):
        return reverse("posts", kwargs={
            "slug":self.slug
        })

    @property
    def num_posts(self):#we get all the post from category
        return Post.objects.filter(categories=self).count() # return the number of total post

    @property
    def last_post(self):
        return Post.objects.filter(categories=self).latest("date")


class Reply(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:100]

    class Meta:
        verbose_name_plural = "replies" #see the ies not y or s


class Comment(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE) #创建一对多的关系的,需要在ForeignKey的第二参数中加入，当删除主表的数据的时候从表中的数据也随着一起删除。
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    replies = models.ManyToManyField(Reply, blank=True)#填写该字段的时候可以不填

    def __str__(self):#以str形式回傳
        return self.content[:100]#100 characters in the comments


class Post(models.Model):
    title = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400, unique=True, blank=True, default=uuid.uuid4)
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = tinymce_models.HTMLField()
    categories = models.ManyToManyField(Category)
    post_images = models.ImageField(upload_to='post_images/', blank=True, null=True)
    # upload_date = models.DateField(default=timezone.now)
    date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )
    tags = TaggableManager()
    comments = models.ManyToManyField(Comment, blank=True)
    closed = models.BooleanField(default=False)
    state = models.CharField(max_length=40, default="zero")
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse("detail", kwargs={
            "slug":self.slug
        })
    #count comment by property for counting
    #post html
    @property
    def num_comments(self):
        return self.comments.count()

    @property
    def last_reply(self):
        return self.comments.latest("date")

