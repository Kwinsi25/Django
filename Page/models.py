from django.db import models
from django.urls import reverse
from tinymce import models as tinymce_models
from Language.models import language

# Create your models here.
class page(models.Model):
    slug = models.SlugField(primary_key=True, unique=True)
    statusChoice = (
        ('enabled','Enabled'),
        ('disabled','Disabled'),
    )
    status = models.CharField(max_length=10,choices=statusChoice,default='enabled')
    sortOrder = models.IntegerField(("Sort Order"),default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.slug)   

    def get_absolute_url(self):
        return reverse("termsConditions", kwargs={"slug": self.slug})    
        
# Create your models here.
def get_language():
    return language.objects.get(isDefault=True)

class pageTranslation(models.Model):
    language = models.ForeignKey(language,on_delete = models.CASCADE,null=False,default=get_language)
    page = models.ForeignKey(page,on_delete = models.CASCADE,null=False)
    contentId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = tinymce_models.HTMLField()

    class Meta:
        verbose_name = "Page Translation"
        unique_together = ('language', 'page',)

    def __str__(self):
        return str(self.title)   
