from django.shortcuts import render
from .models import *

# Create your views here.
listdata=[]
data =[]
lan = language.objects.all()
for i in lan:
    if i.isDefault == "Yes":
        languageid = i.title

def page_list():
    pages = page.objects.filter(status="Enabled").order_by('sortOrder')
    return pages

def page_details(request,slug):
    
    if request.method == 'POST':
        sessiondata = request.POST.get('lang')
        request.session['data'] = sessiondata
        print("sessiondata: ",sessiondata)

    if request.session['data'] is None:
        request.session['data'] = languageid
        print("sessiondata: ",request.session['data'])
    
    pages = page_list()
    contentdata = pageTranslation.objects.all().values()
    languages = language.objects.all().values()
    pagedetails = pageTranslation.objects.raw("select * from Page_pageTranslation where page_id = '"+slug+"'")

    return render(request,'index.html',{'contentdata':pagedetails,'pages':pages,"language":listdata,"datalist":request.session['data'],"language":languages})
    