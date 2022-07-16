from django.db import models
from Language.models import language
from tinymce import models as tinymce_models

# Create your models here.
class bannerGroup(models.Model):
    bannerGroupId = models.AutoField(primary_key=True)
    code = models.SlugField(unique=True)
    
    sortOrder = models.IntegerField(("Sort Order"),default=0)
    statusChoice = (
        ('enabled','Enabled'),
        ('disabled','Disabled'),
    )
    status = models.CharField(max_length=10,choices=statusChoice,default='enabled')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return str(self.code)   

def get_language():
    return language.objects.get(isDefault=True)

class bannerGroupTranslation(models.Model):
    language = models.ForeignKey(language,on_delete = models.CASCADE,null=False,default=get_language)
    bannerGroup = models.ForeignKey(bannerGroup,on_delete = models.CASCADE,null=False)
    bannerGroupTranslationId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Banner Group Translation"
        # unique_together = ('language', 'page',)

    def __str__(self):
        return str(self.name)   

class banner(models.Model):
    bannerId = models.AutoField(primary_key=True)
    sortOrder = models.IntegerField(("Sort Order"),default=0)
    statusChoice = (
        ('enabled','Enabled'),
        ('disabled','Disabled'),
    )
    status = models.CharField(max_length=10,choices=statusChoice,default='enabled')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

class bannerTranslation(models.Model):
    language = models.ForeignKey(language,on_delete = models.CASCADE,null=False,default=get_language)
    bannerTranslationId = models.AutoField(primary_key=True)
    banner = models.ForeignKey(banner,on_delete = models.CASCADE,null=False)
    title = models.CharField(max_length=100)
    content = tinymce_models.HTMLField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Banner Group Translation"
        # unique_together = ('language', 'page',)

    def __str__(self):
        return str(self.title) 

class bannerImage(models.Model):
    bannerImageId = models.AutoField(primary_key=True)
    banner = models.ForeignKey(banner,on_delete = models.CASCADE,null=False)
    bannerGroup = models.ForeignKey(bannerGroup,on_delete = models.CASCADE,null=False)
    image = models.ImageField(upload_to='images/')
    url = models.CharField(max_length=200)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)