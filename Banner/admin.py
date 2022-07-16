from typing import List
from django.contrib import admin
from .models import banner, bannerGroup, bannerGroupTranslation, bannerImage, bannerTranslation
from Language.models import language
import types
from django.utils.html import format_html

from django.db import  IntegrityError
from django.core.exceptions import ObjectDoesNotExist


from django.http import HttpResponseRedirect
from django.contrib import messages
from querystring_parser import parser

from django.template.defaulttags import register
...
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def validate_file_size(value):
        filesize= value.size
        
        if filesize > 8000000:
            return False
        else:
            return True

# Register your models here.

class BannerAdmin(admin.ModelAdmin):
    list_display = ['bannerId','groupandImages','sortOrder','status','createdAt','updatedAt']

    def groupandImages(self,obj):
        imgs = bannerImage.objects.filter(banner_id=obj)
        imgstr = ''
        for i in imgs:
            imgstr = imgstr + '<b>'+i.bannerGroup.code+'<b> : <img src ="'+i.image.url+'" style="height:50px; width:50px;"><br>'
        if imgstr != '':
            return format_html(imgstr)
        else:
            return format_html(f'<center>-</center>')
    groupandImages.short_description = 'Group : Image'

    change_form_template = 'Banner/change_form.html'
    def changeform_view(self, request,obj ,form_url,context=None):
        context = context or {}
        languageData = language.objects.filter(status = "enabled")
        context["language"]=languageData
        bannerGrp = bannerGroup.objects.all()
        context["bannerGroup"]=bannerGrp
        print(context["bannerGroup"])

        if obj is None:
            if request.method == 'POST':
                post_dict = parser.parse(request.POST.urlencode())
                
                sortOrder = post_dict['order']
                status = post_dict['status']

                try:
                    bannerObj = banner(status = status, sortOrder = sortOrder)
                    bannerObj.save()
                except IntegrityError:
                    messages.error(request,"Exception: Error occurs while adding the banner")
                    return HttpResponseRedirect('/admin/Banner/banner/add/')

                try:
                    latestBanner = banner.objects.latest("bannerId")
                    bannerid = banner.objects.get(bannerId=latestBanner.bannerId)
                except ObjectDoesNotExist:
                    messages.error(request,"Exception: Error occurs while fetching banner id")
                    return HttpResponseRedirect('/admin/Banner/banner/add/')

                
                if len(post_dict['bannergroup']) > 0:
                    for i in post_dict['bannergrpid']:
                        bannergrpid = post_dict['bannergrpid'][i]
                        bannerimg = request.FILES['bannerimage['+str(i)+']']
                        url = post_dict['url'][i]

                        try:
                            bannergrpId = bannerGroup.objects.get(bannerGroupId = bannergrpid)
                        except ObjectDoesNotExist:
                            messages.error(request,"Exception: Error occurs while fetching bannergroup id")
                            return HttpResponseRedirect('/admin/Banner/banner/add/')

                        if validate_file_size(bannerimg) and bannerimg.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                            try:
                                bannerImageObj = bannerImage(banner = bannerid ,bannerGroup = bannergrpId, image = bannerimg, url = url)
                                bannerImageObj.save()
                            except IntegrityError:
                                messages.error(request,"Exception: Error occurs while adding the bannerImage")
                                return HttpResponseRedirect('/admin/Banner/banner/add/')

                        else:
                            messages.error(request,"Exception: Enter Image file like(.png, .jpg, .jpeg) and size Under 8 MB")
                            return HttpResponseRedirect('/admin/Banner/banner/')

                for i in languageData:
                
                    title = request.POST[i.locale+'title']
                    content = request.POST[i.locale+'content']
                    
                    langcode = request.POST[i.locale+'lang']

                    try:
                        lang = language.objects.get(locale = langcode)
                    except ObjectDoesNotExist:
                        messages.error(request,"Exception: Error occurs while fetching Language")
                        return HttpResponseRedirect('/admin/Banner/banner/add/')

 
                    try:
                        translation = bannerTranslation(banner = bannerid, title=title, content=content, language = lang)
                        translation.save()
                    except IntegrityError:
                        messages.error(request,"Exception: Error occurs while adding the banner Translation")
                        return HttpResponseRedirect('/admin/Banner/banner/add/')


                messages.success(request," added successfully")
                return HttpResponseRedirect('/admin/Banner/banner/')

        else:
            # bannerDetails = banner.objects.raw("select * from banner_banner as b inner join banner_bannerTranslation as bt on b.bannerId = bt.banner_id inner join banner_bannerImage as bi on b.bannerId = bi.bsnner_id");
            bannerDetails = banner.objects.filter(bannerId=obj)
            context['bannerDetails'] = bannerDetails
            bannerList = {}
            bannerTranslationDetails = bannerTranslation.objects.raw("select * from banner_bannertranslation as bt inner join language_language l on bt.language_id = l.locale where bt.banner_id='"+obj+"'")
            bannerImageList = bannerImage.objects.raw(" select * from banner_bannerGroup bg inner join banner_bannerImage as bi on bg.bannerGroupId = bi.bannerGroup_id where bi.banner_id='"+obj+"' group by bi.bannerGroup_id")
            context['bannerImageList'] = bannerImageList
            for lang in languageData:
                for i in bannerTranslationDetails:
                    if i.locale == lang.locale:
                        bannerList[lang.locale] = {"language":i.locale,'title':i.title,'content':i.content,"bannerTranslationId":i.bannerTranslationId}
            print(bannerList)
            context['bannerList'] = bannerList

            if request.method == 'POST':
                post_dict = parser.parse(request.POST.urlencode())
                print(post_dict)
                check = []
                if(post_dict.get('deletedata',None) is not None):
                    for dltid in post_dict['deletedata'].values():
                        if type(dltid) == type(check):
                            for i in dltid:
                                print("data",i)
                                try:
                                    bannerImage.objects.filter(bannerImageId=i).delete() 
                                except ObjectDoesNotExist:
                                    messages.error(request,"Exception: Error occurs while removing Banner Group")
                                    return HttpResponseRedirect('/admin/Banner/banner/add/')

                        else:
                            try:
                                bannerImage.objects.filter(bannerImageId=dltid).delete() 
                            except ObjectDoesNotExist:
                                messages.error(request,"Exception: Error occurs while removing banner Group")
                                return HttpResponseRedirect('/admin/Banner/banner/'+obj+'/change/')

                bannerid = post_dict['bannerid']
                sortOrder = post_dict['order']
                status = post_dict['status']
                bannergroup = post_dict.get('bannergroup',None)

                banner.objects.filter(bannerId=obj).update(status = status, sortOrder = sortOrder)
                try:
                    bid = banner.objects.get(bannerId=obj)
                except ObjectDoesNotExist:
                    messages.error(request,"Exception: Error occurs while fetching banner id")
                    return HttpResponseRedirect('/admin/Banner/banner/'+obj+'/change/')


                if bannergroup != None:
                    if len(post_dict['bannergroup']) > 0:
                        for i in post_dict['bannergrpid']:
                            bannergrpid = post_dict['bannergrpid'][i]
                            bannerimgs = post_dict.get('bannerimgid',None)
                            if bannerimgs != None:
                                bannerimgid = bannerimgs.get(i,None)
                            else:
                                bannerimgid = None

                            
                            bannerimg = request.FILES.get('bannerimage['+str(i)+']',None)
                            url = post_dict['url'][i]

                            try:
                                bannergrpId = bannerGroup.objects.get(bannerGroupId = bannergrpid)
                            except ObjectDoesNotExist:
                                messages.error(request,"Exception: Error occurs while fetching banner group id")
                                return HttpResponseRedirect('/admin/Banner/banner/'+obj+'/change/')

                            
                            if bannerimgid == None:
                                bannergrpId = bannerGroup.objects.get(bannerGroupId = bannergrpid)
                                # bannerid = banner.objects.get(bannerId = obj)
                                try:
                                    bannerImageObj = bannerImage(banner = bid ,bannerGroup = bannergrpId, image = bannerimg, url = url)
                                    bannerImageObj.save()
                                except IntegrityError:
                                    messages.error(request,"Exception: Error occurs while adding image at update time")
                                    return HttpResponseRedirect('/admin/Banner/banner/'+obj+'/change/')

                            else:
                                if bannerimg != None:
                                    if validate_file_size(bannerimg) and bannerimg.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                                        try:
                                            bnr = bannerImage.objects.get(bannerImageId=bannerimgid)
                                        except ObjectDoesNotExist:
                                            messages.error(request,"Exception: Error occurs while fetching banner image id")
                                            return HttpResponseRedirect('/admin/Banner/banner/'+obj+'/change/')

                                        bnr.image.delete()
                                        bnr.image = bannerimg
                                        bnr.save()
                                        bannerImage.objects.filter(bannerImageId=bannerimgid).update( url = url)
                                    else:
                                        messages.error(request,"Exception: Enter Image file like(.png, .jpg, .jpeg) and size Under 8 MB")
                                        return HttpResponseRedirect('/admin/Banner/banner/')
                                else:

                                    bannerImage.objects.filter(bannerImageId=bannerimgid).update(bannerGroup = bannergrpId, url = url)
                                

                for i in languageData:
                    bannerTranslationId = request.POST[i.locale+'bannertranslationid']
                    title = request.POST[i.locale+'title']
                    content = request.POST[i.locale+'content']
                    
                    langcode = request.POST[i.locale+'lang']

                    try:
                        lang = language.objects.get(locale = langcode)
                    except ObjectDoesNotExist:
                        messages.error(request,"Exception: Error occurs while fetching Language")
                        return HttpResponseRedirect('/admin/Banner/banner/'+obj+'/change/')

                    

                    translation = bannerTranslation.objects.filter(bannerTranslationId=bannerTranslationId).update(banner=bid, title=title, content=content, language=lang)
                    
            
                messages.success(request," updated successfully")
                return HttpResponseRedirect('/admin/Banner/banner/')
        
        

       
        return super(BannerAdmin,self).changeform_view(request, obj ,form_url,context)


class BannerGroupAdmin(admin.ModelAdmin):
    change_form_template = 'BannerGroup/change_form.html'

    list_display = ['code','sortOrder','status','createdAt','updatedAt',]

        
    def changeform_view(self, request,obj ,form_url,context=None):
        context = context or {}
        languageData = language.objects.filter(status = "enabled")
        context["language"]=languageData

        if obj is None:
            
            if request.method == 'POST':
                print(request.POST)
                code = request.POST['code']
                status = request.POST['status']
                sortOrder = request.POST['order']
                
                try:
                    bannerGroupObj = bannerGroup(code = code, status = status, sortOrder = sortOrder)
                    bannerGroupObj.save()
                except IntegrityError:
                    messages.error(request,"Exception: Error occurs while adding the Banner Group")
                    return HttpResponseRedirect('/admin/Banner/bannergroup/add/')


                for i in languageData:
                
                    name = request.POST[i.locale+'name']
                    
                    langcode = request.POST[i.locale+'lang']
                
                    try:
                        lang = language.objects.get(locale = langcode)
                    except ObjectDoesNotExist:
                        messages.error(request,"Exception: Error occurs while fetching Language")
                        return HttpResponseRedirect('/admin/Banner/bannergroup/add/')

                    try:
                        latestBannerGroup = bannerGroup.objects.latest("bannerGroupId")
                        bannerGroupid = bannerGroup.objects.get(bannerGroupId=latestBannerGroup.bannerGroupId)
                    except ObjectDoesNotExist:
                        messages.error(request,"Exception: Error occurs while fetching banner group id")
                        return HttpResponseRedirect('/admin/Banner/bannergroup/add/')
                    
                    try:
                        translation = bannerGroupTranslation(bannerGroup = bannerGroupid, name = name, language = lang)
                        translation.save()
                    except IntegrityError:
                        messages.error(request,"Exception: Error occurs while adding the Banner Group Translation")
                        return HttpResponseRedirect('/admin/Banner/bannergroup/add/')
                    
            
                messages.success(request,code+" added successfully")
                return HttpResponseRedirect('/admin/Banner/bannergroup/')

            else:
                    
                context['bannerGroups'] = bannerGroup.objects.filter(status="enabled")
                print(context['bannerGroups'])
        
        else:
            bannerGroupDetails = bannerGroup.objects.filter(bannerGroupId=obj)
            context['bannerGroupDetails'] = bannerGroupDetails
            print("context",context['bannerGroupDetails'][0].code)
            # pageTranslationDetails = pageTranslation.objects.filter(page=obj)
            # context['pageTranslationDetails'] = pageTranslationDetails
            bannerGroupList = {}
            bannerGroupTranslationDetails = bannerGroupTranslation.objects.raw("select * from banner_bannerGrouptranslation as bt inner join language_language l on bt.language_id = l.locale where bt.bannerGroup_id='"+obj+"'")

            for lang in languageData:
                for i in bannerGroupTranslationDetails:
                    if i.locale == lang.locale:
                        bannerGroupList[lang.locale] = {"language":i.locale,'name':i.name,"bannerGroupTranslationId":i.bannerGroupTranslationId}
            print(bannerGroupList)
            context['bannerGroupList'] = bannerGroupList

            

            if request.method == 'POST':
                code = request.POST['code']
                status = request.POST['status']
                sortOrder = request.POST['order']
                bannerGroupid = request.POST['bannergroupid']

                try:
                    bgid = bannerGroup.objects.get(bannerGroupId=bannerGroupid)
                except ObjectDoesNotExist:
                    messages.error(request,"Exception: Error occurs while fetching Banner Group Id")
                    return HttpResponseRedirect('/admin/Banner/bannergroup/'+obj+'/change/')
                bannerGroupObj = bannerGroup.objects.filter(bannerGroupId=bannerGroupid).update(code = code, sortOrder = sortOrder, status=status)
                

                for i in languageData:
                    bannerGroupTranslationId = request.POST[i.locale+'bannergrouptranslationid']
                    name = request.POST[i.locale+'name']
                    
                    langcode = request.POST[i.locale+'lang']

                    try:
                        lang = language.objects.get(locale = langcode)  
                    except ObjectDoesNotExist:
                        messages.error(request,"Exception: Error occurs while fetching Language")
                        return HttpResponseRedirect('/admin/Banner/bannergroup/'+obj+'/change/')

                    

                    # pgid = page.objects.get(page=slug)
                    
                    translation = bannerGroupTranslation.objects.filter(bannerGroupTranslationId=bannerGroupTranslationId).update(bannerGroup=bgid, name=name, language=lang)
                    
            
                messages.success(request,code+" updated successfully")
                return HttpResponseRedirect('/admin/Banner/bannergroup/')
        

       
        return super(BannerGroupAdmin,self).changeform_view(request, obj ,form_url,context)


admin.site.register(banner,BannerAdmin)
admin.site.register(bannerGroup,BannerGroupAdmin)