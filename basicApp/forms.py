from django import forms

class CarpoolRecommendationForm(forms.Form):
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], label="Gender Preference")
    
    
    age_min = forms.IntegerField(label="Minimum Age Preference", min_value=0, max_value=100)
    age_max = forms.IntegerField(label="Maximum Age Preference", min_value=0, max_value=100)
    
    mode_of_transport = forms.ChoiceField(choices=[('car', 'Car'), ('rickshaw', 'Rickshaw')], label="Preferred Mode of Transport")#example choices
    carpool_now = forms.BooleanField(required=False, label="Carpool Now?")
    current_time = forms.TimeField(required=False, label="Current Time (HH:MM)") 
    cost_sharing = forms.ChoiceField(choices=[('By Time', 'By Time'), ('By Distance', 'By Distance')], label="Cost Sharing Preference") #example choices
