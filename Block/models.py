from .apps import BlockConfig
from django.db import models
from Language.models import language
# Create your models here.
class block(models.Model):
    blockId = models.AutoField(primary_key=True)
    slug = models.CharField(max_length=100,unique=True,default=None)
    statusChoice = (
        ('enabled','Enabled'),
        ('disabled','Disabled'),
    )
    status = models.CharField(max_length=10,choices=statusChoice,default='enabled')
    sortOrder = models.IntegerField(("Sort Order"),default=0)
    created_at = models.DateTimeField(auto_now_add=True)#,input_formats=BlockConfig.DATE_FORMAT#)
    updated_at = models.DateTimeField(auto_now=True)
   

    def __str__(self):
        return str(self.slug) 

def get_language():
    return language.objects.get(isDefault=True)

class blockTranslation(models.Model):
    language = models.ForeignKey(language,on_delete = models.CASCADE,null=False,default=get_language)
    block = models.ForeignKey(block,on_delete = models.CASCADE,null=False)
    contentId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)

    class Meta:
        verbose_name = "Block Translation"
        unique_together = ('language', 'block',)

    def __str__(self):
        return str(self.title)   