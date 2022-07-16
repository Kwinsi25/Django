from Customer.views import edit_data
from django.urls import include, path
urlpatterns = [
    path('edit/',edit_data,name='edit'),
]