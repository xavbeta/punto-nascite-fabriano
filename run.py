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
        print("ERROR: {0} - {1}".format(origin, target))

    return time



pns = pd.read_csv('data/punti-nascita.csv', delimiter=';')
fab_data = pd.read_csv('data/fabriano.csv', delimiter=';')

pprint(pns)
pprint(fab_data)


now = datetime.now()
durations = []
durations_city_center = []
alt_durations_city_center = []
alt_durations_hospital = []
for index, row in fab_data.iterrows():
    city_origin = row['comune']
    hospital_target = pns[pns['pn'] == 'Fabriano'].iloc[0]['address']

    duration = journey_duration(city_origin,hospital_target, now)
    durations.append(duration)

    duration_city_center = journey_duration(city_origin, 'Fabriano', now)
    durations_city_center.append(duration_city_center)
    #[0]['address']
    #print("o: {0} t: {1}".format(city_origin, hospital_target))

    alt_hospital_target = pns[pns['pn'] == row['pnalt']].iloc[0]['address']
    alt_duration_hospital = journey_duration(city_origin, alt_hospital_target, now)
    alt_durations_hospital.append(alt_duration_hospital)

    alt_duration_city_center = journey_duration(city_origin, row['pnalt'], now)
    alt_durations_city_center.append(alt_duration_city_center)
    # [0]['address']
    print("o: {0} t: {1} alt t: {2}".format(city_origin, hospital_target, alt_hospital_target))


fab_data['actual_tempopnindice'] = durations
fab_data['actual_tempopnindice_city_center'] = durations_city_center
fab_data['actual_tempopnalt'] = alt_durations_hospital
fab_data['actual_tempopnalt_city_center'] = alt_durations_city_center

fab_data.to_csv('data/output.csv', sep=';', encoding='utf-8')


pprint(fab_data)
