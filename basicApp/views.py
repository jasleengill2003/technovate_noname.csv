from django.shortcuts import render
from .carpool_algorithm import recommend_carpool_with_rating
import pandas as pd
df = pd.read_csv("/Users/krishijain/Desktop/technovate_nonamecsv/df.csv")
def Welcome(request):
    return render(request,'index.html')

def signup(request):
    return render(request,'signup.html')

def registertohome(request):
    return render(request,'home.html')
def ride(request):
    return render(request,'ride.html')
def chat(request):
    return render(request,'chat.html')
def cc(request):
    return render(request,'cc.html')
def feedback(request):
    return render(request,'feedback.html')
def journey(request):
    return render(request,'journey.html')
def driving(request):
    return render(request,'driving.html')
def drivermap(request):
    return render(request,'drivermap.html')
def contact(request):
    return render(request,'contact.html')
def work(request):
    return render(request,'work.html')
def wallet(request):
    return render(request,'wallet.html')
def safety(request):
    return render(request,'safety.html')

from django.shortcuts import render, redirect
import pandas as pd



def booking(request):
    if request.method == "POST":
        # Extract values from POST data
        gender_preference = request.POST.get('gender-preference').capitalize()

        age_min = int(request.POST.get('age-min'))
        age_max = int(request.POST.get('age-max'))
        mode_of_transport = request.POST.get('mode-of-transport')
        carpool_now = request.POST.get('carpool_now') == "true"
        current_time = request.POST.get('current_time')
        cost_sharing = request.POST.get('cost_sharing')
        pickup_location = request.POST.get('pickup-location')
        destination = request.POST.get('destination')
        
        recommendations = recommend_carpool_with_rating(
            df,
            gender_preference,
            (age_min, age_max),
            mode_of_transport,
            carpool_now,
            current_time,
            cost_sharing,
            pickup_location,
            destination
        )
        
        has_recommendations = not recommendations.empty
        print(has_recommendations)
        print(recommendations)
        
        return render(request, 'results.html', {'recommendations': recommendations, 'has_recommendations': has_recommendations})

    
    return render(request, 'booking.html')
from django.shortcuts import render
from django.shortcuts import render
from .fare_calculation_script import fare_and_time

def fare_estimate(request):
    adjusted_time = None
    fare = None

    if request.method == 'POST':
        start_name = request.POST['start_name']
        end_name = request.POST['end_name']
        mode_of_transport = request.POST['mode_of_transport']

        adjusted_time, fare = fare_and_time(start_name, end_name, mode_of_transport)

    return render(request, 'fare_estimate.html', {'adjusted_time': adjusted_time, 'fare': fare})
