from datetime import datetime, timedelta
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from Customer.models import address
from django.core.mail import send_mail
from Customer.models import customer
import pytz
# Create your views here.
def editdata(request):
    id = request.GET.get('id')
    print(id)
    addresses = address.objects.get(addressId=id)
    address_data = {"addressId":addresses.addressId,"name":addresses.name,"streetAddress":addresses.streetAddress,"houseNo":addresses.houseNo,"postalCode":addresses.postalCode,"landmark":addresses.landmark,"isDefault":addresses.isDefault}
    return JsonResponse(address_data)

def deletedata(request):
    id = request.GET.get('id')
    print("id",id)
    i = address.objects.get(addressId = id[:-1])
    i.delete()
    return redirect("/admin/Customer/customer/")

 
def emailVerification(request):
    code = request.GET.get("code")
    today = datetime.now()
    customerData = customer.objects.filter(code=code)
    status = ""
    if customerData.count() > 0 :
        expiredDate = customerData[0].expireDate
        expireDate_add_5 = expiredDate + timedelta(minutes=1)
        now = pytz.utc.localize(today)
        if expireDate_add_5 > now :
            status = "Email Verification Successfully !!!"
            customer.objects.filter(code=code).update(emailVerified=True,emailVerifiedDate=today,code="00000")
        else:
            status = "Link is expired."
    else:
            status = "Already Verified !!!"
    return render(request, 'demo.html',{"status":status})