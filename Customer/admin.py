from datetime import datetime, timedelta
from django.template.loader import render_to_string 
import random
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.utils.html import strip_tags
from django.contrib import messages
from Customer.models import customerGroup,customer,address
from querystring_parser import parser
from django.template.defaulttags import register


...
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)



class customGroupAdmin(admin.ModelAdmin):
    list_display = ['name','isDefault','created_date','updated_date']
    def created_date(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")
    def updated_date(self, obj):
        return obj.updated_at.strftime("%Y-%m-%d %H:%M:%S")
admin.site.register(customerGroup,customGroupAdmin)

class customerAdmin(admin.ModelAdmin):
	list_display = ['Image','name','group','Verified','created_date','updated_date']
	def name(self,obj):
		return obj.firstName +" "+ obj.lastName
	def Verified(self,obj):
		if obj.emailVerified == False:
			return format_html(f'<i class="ml-2 fa fa-times " style="color:red;">')
		else:
			return format_html(f'<i class="ml-2 fa fa-check " style="color:green;">')
	def Image(self,obj):
		return format_html(f'<img src ="/media/{obj.image}" style="height:30; width:30px;">')
	def created_date(self, obj):
		return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")
	def updated_date(self, obj):
		return obj.updated_at.strftime("%Y-%m-%d %H:%M:%S")
	
	def changeform_view(self, request, obj, form_url, extra_context=None):
		context={}
		customerGroupData = customerGroup.objects.all()
		context['customerGroupData'] = customerGroupData
		
		if obj is None:
			if request.method == 'POST':
				print(request.POST)
				post_dict = parser.parse(request.POST.urlencode())
				firstName = request.POST['firstName']
				lastName = request.POST['lastName']
				image = request.FILES.get('image')
				email = request.POST['email']
				contactNo = request.POST['contactNo']
				password = make_password(request.POST['password'])
				group = request.POST['group']
				customerGroupId = customerGroup.objects.get(customerGroupId=group)
				status = request.POST['status']
				emailVerified = request.POST.get('emailVerified')
				if emailVerified == 'on':
					emailVerified = True
					today = datetime.now()
					customerDataSave = customer(firstName=firstName,lastName=lastName,image=image,email=email,contactNo=contactNo,password=password,group=customerGroupId,emailVerified=emailVerified,emailVerifiedDate = today,status=status)
					customerDataSave.save()
					print("address",request.POST)
					for i in post_dict['option']:
						name = post_dict['option'][i]['name']
						streetAddress = post_dict['option'][i]['streetAddress']
						houseNo = post_dict['option'][i]['houseNo'] 
						postalCode = post_dict['option'][i]['postalCode']
						landmark = post_dict['option'][i]['landmark']
						isDefault = post_dict['option'][i].get('isDefault',None)
						if isDefault == 'on':
							defaultval = True
						else:
							defaultval = False
						customerid = customer.objects.latest('customerId')
						print("cust=",customerid)
						customerId = customer.objects.get(customerId = customerid.customerId)
						print("cid=",customerId)
						addressDataSave = address(name=name,streetAddress=streetAddress,houseNo=houseNo,landmark=landmark,isDefault=defaultval,postalCode=postalCode,customerName=customerId)
						addressDataSave.save()
					messages.success(request,firstName+" added successfully")
					return HttpResponseRedirect('/admin/Customer/customer/')			
				else:
					emailVerified = False
					expireDate = datetime.now()
					print(expireDate)
					email1 = request.POST.get('email')
					code=random.randint(0000,999999)
					username = request.POST.get('firstName')
					html_content = render_to_string("emailVerification.html",{'uname':username,"code":code})
					text_content = strip_tags(html_content)
					emailSend = EmailMultiAlternatives(
						"Email Verification link",text_content,settings.EMAIL_HOST_USER,[email1],
                	)
					emailSend.attach_alternative(html_content,"text/html")
					emailSend.send()
					customerDataSave = customer(firstName=firstName,lastName=lastName,image=image,email=email,contactNo=contactNo,password=password,group=customerGroupId,emailVerified=emailVerified,status=status,code=code,expireDate=expireDate)
					customerDataSave.save()
					for i in post_dict['option']:
						name = post_dict['option'][i]['name']
						streetAddress = post_dict['option'][i]['streetAddress']
						houseNo = post_dict['option'][i]['houseNo'] 
						postalCode = post_dict['option'][i]['postalCode']
						landmark = post_dict['option'][i]['landmark']
						isDefault = post_dict['option'][i].get('isDefault',None)
						if isDefault == 'on':
							defaultval = True
						else:
							defaultval = False
						customerid = customer.objects.latest('customerId')
						print("cust=",customerid)
						customerId = customer.objects.get(customerId = customerid.customerId)
						print("cid=",customerId)
						addressDataSave = address(name=name,streetAddress=streetAddress,houseNo=houseNo,landmark=landmark,isDefault=defaultval,postalCode=postalCode,customerName=customerId)
						addressDataSave.save()
					messages.success(request,firstName+" added successfully")
					return HttpResponseRedirect('/admin/Customer/customer/')			
		else:
			customerGroupData = customerGroup.objects.all()
			context['customerGroupData'] = customerGroupData
			customerData = customer.objects.filter(customerId=obj)
			context['customerData'] = customerData
			addressData = address.objects.raw("select * from Customer_address as a where a.customerName_id ='"+obj+"'")
			context['addressData'] = addressData
			prod = customer.objects.get(customerId=obj)
			context['prod'] = prod
			for i in customerData:
					print(i.email)
					emailOld = i.email
					passwordOld = i.password
			if request.method == 'POST':
				print(request.POST)
				post_dict = parser.parse(request.POST.urlencode())
				customerId=request.POST['customerId']
				firstName = request.POST['firstName']
				lastName = request.POST['lastName']
				image = request.FILES.get('image')
				email = request.POST['email']
				contactNo = request.POST['contactNo']
				password = request.POST['password']
				group = request.POST['group']
				customerGroupId = customerGroup.objects.get(customerGroupId=group)
				status = request.POST['status']
				
				# customer data	
				if image!=None:
					if image.name.lower().endswith(('.png','.jpg','.jpeg')):
						picupdate = customer.objects.get(customerId = obj)
						picupdate.image.delete()
						picupdate.image = image
						picupdate.save()
				emailVerified = request.POST.get('emailVerified')
				print("old",emailOld)
				print("old",passwordOld)
				print("new",password)
				if emailVerified == 'on' and email == emailOld:
					emailVerified = True
					today = datetime.now()
					if password != '':
						getPassword = password.split(" ")
						joinPassword = "".join(getPassword)
						passwordUpdate = make_password(joinPassword)
						customer.objects.filter(customerId=customerId).update(firstName=firstName,lastName=lastName,email=email,password=passwordUpdate,contactNo=contactNo,group=customerGroupId,status=status,emailVerified=emailVerified,emailVerifiedDate=today)
					else:
						customer.objects.filter(customerId=customerId).update(firstName=firstName,lastName=lastName,email=email,contactNo=contactNo,group=customerGroupId,status=status,emailVerified=emailVerified,emailVerifiedDate=today)
				else:
					emailVerified=False
					expireDate = datetime.now()
					print(expireDate)
					email1 = request.POST.get('email')
					code=random.randint(0000,999999)
					username = request.POST.get('firstName')
					html_content = render_to_string("emailVerification.html",{'uname':username,"code":code})
					text_content = strip_tags(html_content)
					emailSend = EmailMultiAlternatives(
						"Email Verification link",text_content,settings.EMAIL_HOST_USER,[email1],
                	)
					emailSend.attach_alternative(html_content,"text/html")
					emailSend.send()
					if password != '':
						getPassword = password.split(" ")
						joinPassword = "".join(getPassword)
						passwordUpdate = make_password(joinPassword)
						customer.objects.filter(customerId=customerId).update(firstName=firstName,lastName=lastName,email=email,password=passwordUpdate,contactNo=contactNo,group=customerGroupId,status=status,emailVerified=emailVerified,code=code,expireDate=expireDate)
					else:
						customer.objects.filter(customerId=customerId).update(firstName=firstName,lastName=lastName,email=email,contactNo=contactNo,group=customerGroupId,status=status,emailVerified=emailVerified,code=code,expireDate=expireDate)
				try:
					for i in post_dict['option']:
						addressId = post_dict['option'][i].get('addressId',None)
						name = post_dict['option'][i]['name']
						streetAddress = post_dict['option'][i]['streetAddress']
						houseNo = post_dict['option'][i]['houseNo']
						postalCode = post_dict['option'][i]['postalCode']
						landmark = post_dict['option'][i]['landmark']
						isDefault = post_dict['option'][i].get('isDefault',None)
						if isDefault == 'on':
							defaultval = True
						else:
							defaultval = False
						if addressId == None:
							try:
								customerId = customer.objects.get(customerId=customerId)
								addressDataSave = address(name=name,streetAddress=streetAddress,houseNo=houseNo,landmark=landmark,isDefault=defaultval,postalCode=postalCode,customerName=customerId)
								addressDataSave.save()
							except:
								messages.add_message(request, messages.ERROR, 'Entered Address already exist!')
								return super(customerAdmin,self).changeform_view(request, obj ,form_url,context)
						else:
							if isDefault == 'on':
								defaultval = True
								address.objects.filter(isDefault=True).filter(customerName=obj).update(isDefault=False)
								address.objects.filter(addressId=addressId).update(name=name,streetAddress=streetAddress,houseNo=houseNo,landmark=landmark,isDefault=defaultval,postalCode=postalCode,customerName=customerId)
							else:
								defaultval = False
							# address data
							address.objects.filter(addressId=addressId).update(name=name,streetAddress=streetAddress,houseNo=houseNo,landmark=landmark,isDefault=defaultval,postalCode=postalCode,customerName=customerId)
				except ValueError:
					print("error")
				messages.success(request,firstName+" update successfully")
				return HttpResponseRedirect('/admin/Customer/customer/')


		return super().changeform_view(request, obj, form_url, extra_context=context)	
admin.site.register(customer,customerAdmin)

# admin.site.register(address)