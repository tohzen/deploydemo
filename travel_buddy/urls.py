from django.urls import path, include           # import include
# from django.contrib import admin              # comment out, or just delete
urlpatterns = [
    path('', include('travel_buddyapp.urls')),	   
    # path('admin/', admin.sites.urls)         
]
