from django.http import HttpResponseRedirect
from querystring_parser import parser
from django.contrib import admin
from django.contrib import messages
from Configurations.models import configurationGroup
from Configurations.models import configurationValue, configuration

# Register your models here.
class configurationGroupAdmin(admin.ModelAdmin):
    list_display = ['name','sortOrder','created_date','updated_date']
    def created_date(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")
    def updated_date(self, obj):
        return obj.updated_at.strftime("%Y-%m-%d %H:%M:%S")
admin.site.register(configurationGroup,configurationGroupAdmin)

class configurationAdmin(admin.ModelAdmin):
    list_display = ['name','accessKey','FieldType','group','created_date','updated_date']
    def created_date(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")
    def updated_date(self, obj):
        return obj.updated_at.strftime("%Y-%m-%d %H:%M:%S")

    def changeform_view(self, request, obj, form_url, context=None):
        context = context or {}
        configurationGroupData = configurationGroup.objects.all()
        context['configurationGroupData'] = configurationGroupData
        if obj is None:
            print(request.POST)
            if request.method == 'POST':
                post_dict = parser.parse(request.POST.urlencode())
                name = post_dict['name']
                accessKey = post_dict['accessKey']
                FieldType = post_dict['FieldType']
                group = post_dict['group']
                if FieldType in ['text']:
                    value = post_dict['textValue']
                    configurationSave = configuration(name=name,accessKey=accessKey,FieldType=FieldType,group_id=group,value=value)
                    configurationSave.save()
                elif FieldType in ['boolean']:
                    value = post_dict['booleanValue']
                    configurationSave = configuration(name=name,accessKey=accessKey,FieldType=FieldType,group_id=group,value=value)
                    configurationSave.save()
                elif FieldType in ['select']:
                    for i in post_dict['value']:
                        key = post_dict['value'][i]['key']
                        value = post_dict['value'][i]['value']
                        sortOrder = post_dict['value'][i]['sortOrder']
                        isDefault = post_dict['value'][i].get('isDefault',None)
                        if isDefault == 'on':
                            isDefaultval = True
                        else:
                            isDefaultval = False
                        configurationSave = configuration(name=name,accessKey=accessKey,FieldType=FieldType,group_id=group)
                        configurationSave.save()
                        confIdLatest = configuration.objects.latest('configurationId')
                        configurationId = configuration.objects.get(configurationId = confIdLatest.configurationId)
                        valueSave = configurationValue(key=key,value=value,sortOrder=sortOrder,isDefault=isDefaultval,configurationName=configurationId)
                        valueSave.save()
                messages.success(request,name+" added successfully")
                return HttpResponseRedirect('/admin/Configurations/configuration/')
        else:
                configurationGroupDetails = configurationGroup.objects.all()
                context['configurationGroupDetails'] = configurationGroupDetails
                configurationDetails = configuration.objects.filter(configurationId=obj)
                context['configurationDetails'] = configurationDetails
                configurationValueDetails = configurationValue.objects.raw("select * from configurations_configurationValue as cv where cv.configurationName_id ='"+obj+"'")
                context['configurationValueDetails'] = configurationValueDetails
                if request.method == 'POST':
                    post_dict = parser.parse(request.POST.urlencode())
                    if(post_dict.get('deletedata') is not None):
                        for dlt in post_dict['deletedata']:
                            configurationValue.objects.filter(configurationValueId=post_dict['deletedata'][dlt]).delete() 
                    configurationId = post_dict['configurationId']
                    name = post_dict['name']
                    accessKey = post_dict['accessKey']
                    FieldType = post_dict['FieldType']
                    group = post_dict['group']
                    if FieldType in ['text']:
                        valueText = post_dict['textValue']
                        configuration.objects.filter(configurationId = configurationId).update(name=name,accessKey=accessKey,FieldType=FieldType,group=group,value=valueText)
                    elif FieldType in ['boolean']:
                        valueBoolean = post_dict['booleanValue']
                        configuration.objects.filter(configurationId = configurationId).update(name=name,accessKey=accessKey,FieldType=FieldType,group=group,value=valueBoolean)
                    else:
                        configuration.objects.filter(configurationId = configurationId).update(name=name,accessKey=accessKey,FieldType=FieldType,group=group)
                    if FieldType in ['select']:                  
                        for i in post_dict['value']:
                            configurationValueId = post_dict['value'][i].get('configurationValueId',None)
                            key = post_dict['value'][i]['key']
                            value = post_dict['value'][i]['value']
                            sortOrder = post_dict['value'][i]['sortOrder']
                            isDefault = post_dict['value'][i].get('isDefault',None)
                            if isDefault == 'on':
                                isDefaultval = True
                            else:
                                isDefaultval = False
                            
                            if configurationValueId == None:
                                    configurationValues = configurationValue(key = key,value=value,sortOrder=sortOrder,isDefault=isDefaultval,configurationName_id=configurationId)
                                    configurationValues.save()
                            else:
                                configurationValue.objects.filter(configurationValueId=configurationValueId).update(key = key,value=value,sortOrder=sortOrder,isDefault=isDefaultval,configurationName=configurationId)
                    else:
                        try:
                            for i in post_dict['value']:
                                configurationValueId = post_dict['value'][i].get('configurationValueId',None)
                                configurationValue.objects.filter(configurationValueId=configurationValueId).delete() 
                        except KeyError:
                            print("error")
                    messages.success(request,name+" update successfully")
                    return HttpResponseRedirect('/admin/Configurations/configuration/')
        return super(configurationAdmin,self).changeform_view(request, obj ,form_url,context)
admin.site.register(configuration,configurationAdmin)

admin.site.register(configurationValue)