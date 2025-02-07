from django.db import models
from django.urls import reverse
# from taggit.managers import TaggableManager

# Create your models here.



class Post(models.Model):
    # image = models.ImageField(upload_to='blog/%Y/%m/%d/',default='blog/defaultPost.jpg')
    image = models.ImageField(upload_to='blog/%Y/%m/%d/',null=True, blank=True)
    #author = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey('accounts.Profile', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    # topic = models.ForeignKey('homepage.Topic', on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    # tags = TaggableManager()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    counted_views = models.IntegerField(default=0) # default=0
    status = models.BooleanField(default=False)
    login_require = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('-created_date',)
        #verbose_name = "پست"
        #verbose_name_plural = "پست ها"
    def __str__(self):
        return f'{self.title} - {self.id}'

    def get_snippet(self):
        return self.content[:10]+'...'
    
    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={'post_id':self.id})
    
    def get_relative_api_url(self):
        return reverse('blog:api-v1:post-detail', kwargs={'pk':self.id})
    
    def increment_views(self):
        self.counted_views += 1
        self.save(update_fields=['counted_views'])
    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return None 
    
    
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    
    
class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)  # Link to Profile
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)  # Link to User model
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.profile.first_name} {self.profile.last_name} - post: {self.post}'

    class Meta:
        ordering = ('-created_date',)