from django.contrib import messages
from django.contrib import admin
from django.http import HttpResponseRedirect
from Language.models import language
from Block.models import block, blockTranslation
from django.template.defaulttags import register

from Block.apps import BlockConfig

...
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# Register your models here.
class blockAdmin(admin.ModelAdmin):
    list_display = ['slug','status','sortOrder','created_at','updated_date',]
    
    def updated_date(self, obj):
        return obj.updated_at.strftime("%Y-%m-%d %H:%M:%S")

    def changeform_view(self, request,obj ,form_url,context=None):
        context = context or {}
        languageData = language.objects.filter(status = "enabled")
        context["language"]=languageData

        if obj is None:
            
            if request.method == 'POST':
                slug = request.POST['slug']
                status = request.POST['status']
                sortOrder = request.POST['order']

                blockObj = block(slug=slug,status=status,sortOrder=sortOrder)
                blockObj.save()

                for i in languageData:
                
                    title = request.POST[i.locale+'title']
                    content = request.POST[i.locale+'content']
                    print("title",title,content)
                    langcode = request.POST[i.locale+'lang']
                
                    lang = language.objects.get(locale = langcode)
                    

                    

                    blocks = block.objects.get(slug=slug)
                    
                    translation = blockTranslation(block=blocks,title=title,content=content,language=lang)
                    translation.save()
            
                messages.success(request,slug+" added successfully")
                return HttpResponseRedirect('/admin/Block/block/')

            else:
                    
                    context['blocks'] = block.objects.filter(status="enabled")
                    print(context['blocks'])
        
        else:
            blockDetails = block.objects.filter(blockId=obj)
            context['blockDetails'] = blockDetails
            print("bsdjjhd",blockDetails)
            blockList = {}
            blockTranslationDetails = blockTranslation.objects.raw("select * from block_blocktranslation as pt inner join language_language l on pt.language_id = l.locale where pt.block_id='"+obj+"'")

            for lang in languageData:
                for i in blockTranslationDetails:
                    if i.locale == lang.locale:
                        blockList[lang.locale] = {"language":i.locale,'title':i.title,"content":i.content,"contentId":i.contentId}
                
            context['blockList'] = blockList

            

            if request.method == 'POST':
                slug = request.POST['slug']
                status = request.POST['status']
                sortOrder = request.POST['order']

                pageObj = block.objects.filter(slug=slug).update(status=status,sortOrder=sortOrder)
                

                for i in languageData:
                    contentId = request.POST[i.locale+'contentId']
                    title = request.POST[i.locale+'title']
                    content = request.POST[i.locale+'content']
                    print("title",title,content)
                    langcode = request.POST[i.locale+'lang']
                
                    lang = language.objects.get(locale = langcode)
                    

                    

                    blocks = block.objects.get(slug=slug)
                    
                    translation = blockTranslation.objects.filter(contentId=contentId).update(block=blocks,title=title,content=content,language=lang)
                    
            
                messages.success(request,slug+" updated successfully")
                return HttpResponseRedirect('/admin/Block/block/')
        

       
        return super(blockAdmin,self).changeform_view(request, obj ,form_url,context)

admin.site.register(block,blockAdmin)
