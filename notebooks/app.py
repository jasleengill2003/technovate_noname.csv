min_sum = 0
src_minval=99
des_minval=99
# ors format - [long, lat]
# folium - [lat, long]
# api key setup 
client = ors.Client(key='5b3ce3597851110001cf62480f73447f67a2444fa6cc065b11091e9f')
# default location to load map
m = folium.Map(location=list(reversed([72.8429,19.0194])), tiles="cartodbpositron", zoom_start=13)

# user coords
user_cords = [[72.830098,18.964234], [72.836745, 18.992558]]

user_route = client.directions(coordinates=user_cords,
                          profile='foot-walking',
                          format='geojson')

user_route_steps = user_route['features'][0]['geometry']['coordinates']
ucords = np.array(user_cords)
# add user line and markers
add_line(path=user_route)
add_marker(cords=user_cords[0], message=f'User-start {user_cords[0]}', color="orange")
add_marker(cords=user_cords[1], message=f'User-end {user_cords[1]}', color="purple")

# route coords
coords = [
    [[72.839412, 18.944179], [72.8362869, 19.0240881]],
    [[72.879096, 19.038091], [72.844032, 19.030788]],
    [[72.834946, 18.981618], [72.809643, 18.980450]]
]

for i in range(len(coords)):
    print(coords[i])
    route = client.directions(coordinates=coords[i],
                              profile='foot-walking',
                              format='geojson')
    
    route_steps = route['features'][0]['geometry']['coordinates']

    add_line(path=route)
    add_marker(cords=coords[i][0], message=f'Route-start {coords[i][0]}', color="green")
    add_marker(cords=coords[i][1], message=f'Route-end {coords[i][1]}', color="red")

    src_route_start = client.directions(coordinates=[user_cords[0], route_steps[0]],
                              profile='foot-walking',
                              format='geojson')
    des_route_end = client.directions(coordinates=[user_cords[1], route_steps[-1]],
                              profile='foot-walking',
                              format='geojson')
    print(src_route_start["features"][0]["properties"]["segments"][0]["distance"], des_route_end["features"][0]["properties"]["segments"][0]["distance"])

    steps = np.array(route_steps)
    src_diff = np.sum(np.abs(steps-ucords[0]),axis=1)
    des_diff = np.sum(np.abs(steps-ucords[1]),axis=1)

    add_line(path=route)
    add_marker(cords=coords[i][0], message=f'Route-start {coords[i][0]}', color="green")
    add_marker(cords=coords[i][1], message=f'Route-end {coords[i][1]}', color="red")

    min_src = np.argmin(src_diff)
    min_des = np.argmin(des_diff)

    if src_minval>src_diff[min_src]:
        src_minval = src_diff[min_src]
        min_src_cord = steps[min_src]
    if des_minval>des_diff[min_des]:
        des_minval = des_diff[min_des]
        min_des_cord = steps[min_des]

    print(src_minval, des_minval, min_src_cord, min_des_cord)

add_marker(cords=min_src_cord, message=f"Minsrc- {min_src_cord}", color="black")
add_marker(cords=min_des_cord, message=f"Mindes- {min_des_cord}", color="black")
add_line(path=client.directions([list(min_src_cord), list(min_des_cord)], 'foot-walking', 'geojson'), color="black")

m
