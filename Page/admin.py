from django.contrib import admin
from django.http import HttpResponseRedirect
from Page.models import page,pageTranslation
from Language.models import language
from django.contrib import messages
from django.template.defaulttags import register
...
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


    
class PageAdmin(admin.ModelAdmin):
    list_display = ['slug','status','sortOrder','created_at','updated_at',]

        
    def changeform_view(self, request,obj ,form_url,context=None):
        context = context or {}
        languageData = language.objects.filter(status = "enabled")
        context["language"]=languageData

        if obj is None:
            
            if request.method == 'POST':
                slug = request.POST['slug']
                status = request.POST['status']
                sortOrder = request.POST['order']

                pageObj = page(slug=slug,status=status,sortOrder=sortOrder)
                pageObj.save()

                for i in languageData:
                
                    title = request.POST[i.locale+'title']
                    content = request.POST[i.locale+'content']
                    print("title",title,content)
                    langcode = request.POST[i.locale+'lang']
                
                    lang = language.objects.get(locale = langcode)
                    

                    

                    pg = page.objects.get(slug=slug)
                    
                    translation = pageTranslation(page=pg,title=title,content=content,language=lang)
                    translation.save()
            
                messages.success(request,slug+" added successfully")
                return HttpResponseRedirect('/admin/Page/page/')

            else:
                    
                    context['pages'] = page.objects.filter(status="enabled")
                    print(context['pages'])
        
        else:
            pageDetails = page.objects.filter(slug=obj)
            context['pageDetails'] = pageDetails
            # pageTranslationDetails = pageTranslation.objects.filter(page=obj)
            # context['pageTranslationDetails'] = pageTranslationDetails
            pageList = {}
            pageTranslationDetails = pageTranslation.objects.raw("select * from page_pagetranslation as pt inner join language_language l on pt.language_id = l.locale where pt.page_id='"+obj+"'")

            for lang in languageData:
                for i in pageTranslationDetails:
                    if i.locale == lang.locale:
                        pageList[lang.locale] = {"language":i.locale,'title':i.title,"content":i.content,"contentId":i.contentId}
                
            context['pageList'] = pageList

            

            if request.method == 'POST':
                slug = request.POST['slug']
                status = request.POST['status']
                sortOrder = request.POST['order']

                pageObj = page.objects.filter(slug=slug).update(status=status,sortOrder=sortOrder)
                

                for i in languageData:
                    contentId = request.POST[i.locale+'contentId']
                    title = request.POST[i.locale+'title']
                    content = request.POST[i.locale+'content']
                    print("title",title,content)
                    langcode = request.POST[i.locale+'lang']
                
                    lang = language.objects.get(locale = langcode)

                    pg = page.objects.get(slug=slug)
                    
                    translation = pageTranslation.objects.filter(contentId=contentId).update(page=pg,title=title,content=content,language=lang)
                    
            
                messages.success(request,slug+" updated successfully")
                return HttpResponseRedirect('/admin/Page/page/')
        

       
        return super(PageAdmin,self).changeform_view(request, obj ,form_url,context)

admin.site.register(page,PageAdmin)