from django.contrib import admin
from Attribute.models import attribute,attributeTranslation,option,optionTranslation
from django.http import HttpResponse, HttpResponseRedirect
from Language.models import language
from django.db import  IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from querystring_parser import parser
from django.template.defaulttags import register
...
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


class Error(Exception):
   pass


class FetchDataError(Error):
     pass

# Register your models here.
class AttributeAdmin(admin.ModelAdmin):
    list_display = ['code','inputType','isRequired','created_date','updated_date']
    def created_date(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")
    def updated_date(self, obj):
        return obj.updated_at.strftime("%Y-%m-%d %H:%M:%S")


    # changelist
    # def changelist_view(self, request,extra_context=None):    
    #     extra_context={}
    #     attributeData = attribute.objects.raw("select a.attributeId,a.code,a.inputType,a.isRequired,o.attribute_id,GROUP_CONCAT(o.customOption order by o.optionId SEPARATOR ', ') as `options` from attribute_attribute a left JOIN attribute_option o  on a.attributeId=o.attribute_id  group by a.code")
    #     extra_context['attribute']=attributeData
    #     return super().changelist_view(request, extra_context=extra_context)

    # changeform
    def changeform_view(self, request, obj, form_url, context=None):
        context = context or {}
        languageData = language.objects.filter(status = "enabled")
        context["language"]=languageData

        if obj is None:
            if request.method == 'POST':
                post_dict = parser.parse(request.POST.urlencode())
                code= post_dict['code']
                input = post_dict['inputtype']
                required = post_dict['required']

                try:
                    attr = attribute(code=code,inputType=input,isRequired=required)
                    attr.save()
                except :
                    messages.add_message(request, messages.ERROR, 'Entered Code already exist!')
                    return HttpResponseRedirect('/admin/Attribute/attribute/')

                try:
                    attrId = attribute.objects.get(code=code)
                except ObjectDoesNotExist:
                    return HttpResponse("Exception: Error occurs while fetching attribute id")

                for i in languageData:
                    
                    name = request.POST[i.locale+'name']
                    lang = request.POST[i.locale+'language']
                    langId = language.objects.get(locale=lang)

                    
                    attrTrans = attributeTranslation(name=name,language=langId,attribute=attrId)
                    attrTrans.save()
                
                if input in ['radio','checkbox','select','multiselect']:
                    
                    for i in post_dict['option']:
                        
                        customOption = post_dict['option'][i]['customoption']
                        order = post_dict['option'][i]['order']
                        default = post_dict['option'][i].get('default',None)
                        if default == 'on':
                            defaultval = True
                        else:
                            defaultval = False
                        try:
                            opt = option(customOption=customOption,sortOrder=order,isDefault=defaultval,attribute=attrId)
                            opt.save()
                        except:
                            messages.add_message(request, messages.ERROR, 'Entered Options already exist!')
                            return HttpResponseRedirect('/admin/Attribute/attribute/add/')

                        
                        optId = option.objects.get(customOption=customOption)
                        
                        
                        for lang in languageData:
                            
                            optName = post_dict['option'+lang.locale][i]['opname']
                            optLang = post_dict['option'+lang.locale][i]['oplanguage']
                            optLangId = language.objects.get(locale=optLang)
                            
                            
                            optTrans = optionTranslation(name=optName,language=optLangId,option=optId)
                            optTrans.save()
                            
                messages.success(request,code+" added successfully")
                return HttpResponseRedirect('/admin/Attribute/attribute/')
                

        else:
            attributeDetails = attribute.objects.filter(attributeId=obj)
            context['attributeDetails'] = attributeDetails
            optionDetails = option.objects.raw("select * from attribute_option as o where o.attribute_id ='"+obj+"'")
            context['optionDetails'] = optionDetails
            attributeNames = {}
            attributeTranslationDetails = attributeTranslation.objects.raw("select * from attribute_attributetranslation as at inner join language_language l on at.language_id = l.locale where at.attribute_id='"+obj+"'")

            for lang in languageData:
                for i in attributeTranslationDetails:
                    
                    if lang.locale == i.locale:
                        attributeNames["attributeTranslationId"] = i.attributeTranslationId
                        attributeNames[lang.locale] = {"language":i.locale,'name':i.name,'attributeTranslationId':i.attributeTranslationId}
            

            context['attributeNames'] = attributeNames

            optionNames = {}
            optionTranslationDetails = optionTranslation.objects.raw("select * from attribute_optiontranslation as ot inner join language_language l on ot.language_id = l.locale inner join attribute_option as o on o.optionId=ot.option_id where o.attribute_id='"+obj+"'")
            

            for lang in languageData:
                optionNames[lang.locale] = {}
                for i in optionTranslationDetails:
                    
                    if i.locale == lang.locale:
                        optionNames[lang.locale][i.customOption]= {"language":i.locale,'name':i.name,"optionTranslationId":i.optionTranslationId}
            
            
            context['optionNames'] = optionNames

            try:
                if context['attributeDetails'] is None or context['optionDetails'] is None or context['attributeNames'] is None or context['optionNames'] is None:
                    raise FetchDataError
            except FetchDataError:
                return HttpResponse("Exception: Error occurs while fetching attribute details")

            if request.method == 'POST':
                post_dict = parser.parse(request.POST.urlencode())
                

                if(post_dict.get('deletedata') is not None):
                    for dlt in post_dict['deletedata']:
                        option.objects.filter(optionId=post_dict['deletedata'][dlt]).delete() 

                attrId = post_dict['attributeid']
                code= post_dict['code']
                input = post_dict['inputtype']
                required = post_dict['required']
                
                attr = attribute.objects.filter(attributeId=attrId).update(code=code,inputType=input,isRequired=required)
               

                for i in languageData:
                    name = post_dict[i.locale+'name']
                    lang = post_dict[i.locale+'language']
                    langId = language.objects.get(locale=lang)
                    
                    attrTransId = request.POST[i.locale+'attributetranslationid']
                

                    attrTrans = attributeTranslation.objects.filter(attributeTranslationId=attrTransId).update(name=name,language=langId,attribute=attrId)
                
                if input in ['radio','checkbox','select','multiselect']:                  
                    for i in post_dict['option']:
                        
                        optId = post_dict['option'][i].get('optionid',None)
                        customOption = post_dict['option'][i]['customoption']
                        order = post_dict['option'][i]['order']
                        default = post_dict['option'][i].get('default',None)
                        
                        if default == 'on':
                            defaultval = True
                        else:
                            defaultval = False
                        
                        if optId == None:
                            try:
                                attribute_id = attribute.objects.get(attributeId=attrId)
                                opt = option(customOption=customOption,sortOrder=order,isDefault=defaultval,attribute=attribute_id)
                                opt.save()
                            except:
                                messages.add_message(request, messages.ERROR, 'Entered Options already exist!')
                                return super(AttributeAdmin,self).changeform_view(request, obj ,form_url,context)
                        else:
                            opt = option.objects.filter(optionId=optId).update(customOption=customOption,sortOrder=order,isDefault=defaultval,attribute=attrId)

                        for lang in languageData:
                            optName = post_dict['option'+lang.locale][i]['opname']
                            optLang = post_dict['option'+lang.locale][i]['oplanguage']
                            optTransId = post_dict['option'+lang.locale][i].get('optiontranslationid',None)
                            optLangId = language.objects.get(locale=optLang)

                            if optTransId == None:
                                    optId = option.objects.get(customOption=customOption)
                                    optTrans = optionTranslation(name=optName,language=optLangId,option=optId)
                                    optTrans.save()
                            else:
                                optTrans = optionTranslation.objects.filter(optionTranslationId=optTransId).update(name=optName,language=optLangId,option=optId)
                else:
                    try:
                        for i in post_dict['option']:
                            optId = post_dict['option'][i].get('optionid',None)
                            option.objects.filter(optionId=optId).delete() 
                    except KeyError:
                        print("error")
                messages.success(request,code+" updated successfully")
                return HttpResponseRedirect('/admin/Attribute/attribute/')        
        return super(AttributeAdmin,self).changeform_view(request, obj ,form_url,context)
admin.site.register(attribute,AttributeAdmin)
