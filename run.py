import pandas as pd
import googlemaps
from datetime import datetime
from pprint import pprint
from var_dump import var_dump
from typing import Any

gmaps = googlemaps.Client(key='AIzaSyCemUwaxKlYav7kD-aOkjKYKlSzLGfX-xE')


def journey_duration(origin, target, when):
    time = 0
    try:
        directions_result = gmaps.directions(origin,
                                         target,
                                         mode="driving",
                                         departure_time=when
                                         )
        time = int(directions_result[0]['legs'][0]['duration']['value'] / 60)
    except:
        pass

    return time



pns = pd.read_csv('data/punti-nascita.csv', delimiter=';')
fab_data = pd.read_csv('data/fabriano.csv', delimiter=';')

pprint(pns)
pprint(fab_data)


now = datetime.now()
durations = []
alt_durations = []
for index, row in fab_data.iterrows():
    city_origin = row['comune']
    hospital_target = pns[pns['pn'] == 'Fabriano'].iloc[0]['address']

    duration = journey_duration(city_origin,hospital_target, now)
    durations.append(duration)
    #[0]['address']
    #print("o: {0} t: {1}".format(city_origin, hospital_target))

    alt_hospital_target = pns[pns['pn'] == row['pnalt']].iloc[0]['address']

    alt_duration = journey_duration(city_origin, alt_hospital_target, now)
    alt_durations.append(alt_duration)
    # [0]['address']
    print("o: {0} t: {1} alt t: {2}".format(city_origin, hospital_target, alt_hospital_target))


fab_data['actual_tempopnindice'] = durations
fab_data['actual_tempopnalt'] = alt_durations

fab_data.to_csv('data/output.csv', sep=';', encoding='utf-8')


# Geocoding an address
#geocode_result = gmaps.geocode('Viale Stelluti Scala, 26, 60044 Fabriano AN, Italy')
#print(geocode_result)
# Look up an address with reverse geocoding
#reverse_geocode_result = gmaps.reverse_geocode((45, 12))
#print(reverse_geocode_result)
# Request directions via public transit
#now = datetime.now()
#directions_result = gmaps.directions("Matelica",
#                                     "Viale Stelluti Scala, 26, 60044 Fabriano AN",
#                                     mode="driving",
#                                     #departure_time=now
#                                     )

#print(int(directions_result[0]['legs'][0]['duration']['value'] / 60))

#print(directions_result[0]['legs'][0]['duration']['value'])

pprint(fab_data)
