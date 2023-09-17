# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

df = pd.read_csv("/Users/krishijain/Desktop/technovate_nonamecsv/df.csv")

import pandas as pd
from datetime import datetime, timedelta

def recommend_carpool_with_rating(data, gender, age_range, mode_of_transport, carpool_now, current_time, cost_sharing, specific_address, destination_address):
    
    #filtered_data=data
   
    filtered_data = data[data['Gender'] == gender]

    
    min_age, max_age = age_range
    filtered_data = filtered_data[(filtered_data['Age'] >= min_age) & (filtered_data['Age'] <= max_age)]

    
    preferred_mode_data = filtered_data[filtered_data['Preferred Mode of Travel'] == mode_of_transport]
    other_modes_data = filtered_data[filtered_data['Preferred Mode of Travel'] != mode_of_transport]

    
    if carpool_now:
        current_time_obj = datetime.strptime(current_time, '%H:%M')
        time_lower_bound = (current_time_obj - timedelta(minutes=10)).strftime('%H:%M')
        time_upper_bound = (current_time_obj + timedelta(minutes=10)).strftime('%H:%M')

        preferred_mode_data = preferred_mode_data[(preferred_mode_data['Time of Departure'] >= time_lower_bound) &
                                                  (preferred_mode_data['Time of Departure'] <= time_upper_bound)]
        other_modes_data = other_modes_data[(other_modes_data['Time of Departure'] >= time_lower_bound) &
                                            (other_modes_data['Time of Departure'] <= time_upper_bound)]

    
    preferred_mode_data = preferred_mode_data[preferred_mode_data['Cost Sharing Preference'] == cost_sharing]
    other_modes_data = other_modes_data[other_modes_data['Cost Sharing Preference'] == cost_sharing]

    
    recommendations = pd.concat([preferred_mode_data, other_modes_data])

    
    recommendations = recommendations.sort_values(by='final rating', ascending=False)

    
    max_people = int(recommendations.iloc[0]['max_ppl']) if not recommendations.empty else 0
    print(recommendations.columns)
    return recommendations.head(max_people - 1)
#example usage
recommendations = recommend_carpool_with_rating(
    df,
    'Male',
    (20, 30),
    'car',
    True,
    '19:40',
    'By Time',
    '39 D Avenue, Navi Mumbai',
    'Street B, Central Mumbai'
)




print(recommendations[['User ID', 'Name', 'Age', 'Gender', 'Preferred Mode of Travel', 'Time of Departure', 'Specific Address', 'Destination Address']])
