from haversine import haversine, Unit
import pandas as pd

def find_airport_by_ident(data, ident):
    df = data[data['ident'] == ident ]
    return df.to_dict('records')[0]

def calculate_distance(source_ident, destination_ident):
    source = source_ident['latitude_deg'], source_ident['longitude_deg']
    destination = destination_ident['latitude_deg'], destination_ident['longitude_deg']

    result = haversine(source, destination, unit=Unit.MILES)
    return result

def calculate_time(distance, speed):
    return round(distance/speed, 3)

def choose_random_airport(data, count, sort):
    df = data.sample(n=count)
    if sort:
        return df.sort_values('duration_to')
    else:
        return df

df = pd.read_csv('airports.csv')

selected_columns = [
    'ident',
    'type',
    'name',
    'latitude_deg',
    'longitude_deg',
    'elevation_ft',
    'iso_country',
    'iso_region',
    'icao_code',
    'iata_code',
    'gps_code',
    'local_code',
    'scheduled_service',
]

filtered_columns_df = df[selected_columns]
us_airports = filtered_columns_df[(filtered_columns_df['iso_country'] == 'US') & (filtered_columns_df['type'] != 'heliport') & (filtered_columns_df['type'] != 'seaplane_base') & (filtered_columns_df['type'] != 'closed')]

knots = 200
bos = find_airport_by_ident(us_airports, 'KBOS')
det = find_airport_by_ident(us_airports, 'KDTW')
distance = calculate_distance(bos, det)
duration = calculate_time(distance, 200)

source = bos

results = []

for airport in us_airports.to_dict('records'):
    distance = calculate_distance(source, airport)
    duration = calculate_time(distance, knots)
    result = {'ident': airport['ident'], 'distance_to': distance, 'duration_to': duration}
    results.append(result)

results_df = pd.DataFrame(results)
new_df = pd.merge(us_airports, results_df, on='ident')

close_airports = new_df[new_df['duration_to'] <= 1]
print(choose_random_airport(close_airports, 10, False))