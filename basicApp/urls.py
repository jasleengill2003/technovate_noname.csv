from django.urls import path
from . import views
urlpatterns = [
    path('',views.Welcome),
    path('signup/',views.signup,name='signup'),
    path('booking/', views.booking, name='booking'),
    path('registertohome/',views.registertohome,name='registertohome'),
    path('calculate_fare/',views.fare_estimate,name='fare_estimate'),
    path('ride/',views.ride,name='ride'),
    path('chat/',views.chat,name='chat'),
    path('cc/',views.cc,name='cc'),
    path('feedback/',views.feedback,name='feedback'),
    path('journey/',views.journey,name='journey'),
    path('driving/',views.driving,name='driving'),
    path('drivermap/',views.drivermap,name='drivermap'),
    path('contact/',views.contact,name='contact'),
    path('work/',views.work,name='work'),
    path('wallet/',views.wallet,name='wallet'),
    path('safety/',views.safety,name='safety'),
    
]
