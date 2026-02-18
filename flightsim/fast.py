from fastapi import FastAPI
from haversine import haversine, Unit
import pandas as pd
import random

app = FastAPI()


def load_file():
    """
    Load and filter US airport data from CSV file.

    Returns:
        pd.DataFrame: Filtered DataFrame containing US airport data excluding heliports, seaplane bases, and closed airports.
    """
    # https://ourairports.com/airports.html
    df = pd.read_csv('us-airports.csv')

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
    us_airports = filtered_columns_df[(filtered_columns_df['iso_country'] == 'US') & (filtered_columns_df['type'] != 'heliport') & (
        filtered_columns_df['type'] != 'seaplane_base') & (filtered_columns_df['type'] != 'closed')]

    us_airports = us_airports.fillna(0)
    return us_airports


def get_airport(icao: str):
    """
    Retrieve airport data by ICAO code.

    Args:
        icao (str): ICAO airport code (case-insensitive).

    Returns:
        dict: Airport information including name, coordinates, elevation, and codes. Returns None if airport not found.
    """
    data = load_file()
    try:
        df = data[data['ident'] == icao.upper()]
        return df.to_dict('records')[0]
    except Exception as e:
        print(f'Failed to get airport: {icao}. Error: {e}')
        return None


def calculate_distance(source_airport, latitude_deg, longitude_deg):
    """
    Calculate distance between source airport and destination coordinates using haversine formula.

    Args:
        source_airport (dict): Airport dictionary containing 'latitude_deg' and 'longitude_deg' keys.
        latitude_deg (float): Destination latitude in degrees.
        longitude_deg (float): Destination longitude in degrees.

    Returns:
        float: Distance in miles, rounded to 4 decimal places.
    """
    source_coordinates = source_airport['latitude_deg'], source_airport['longitude_deg']
    destination_coordinates = latitude_deg, longitude_deg
    result = haversine(source_coordinates,
                       destination_coordinates, unit=Unit.MILES)
    return round(result, 4)


def calculate_range(source: str, area: int):
    """
    Find all airports within a specified range from source airport.

    Args:
        source (str): ICAO code of source airport.
        area (int): Search radius in miles.

    Returns:
        pd.DataFrame: DataFrame of airports within range, sorted by distance_to column.
    """
    data = load_file()
    results = []

    source_airport = get_airport(source)
    data['distance_to'] = data.apply(lambda row: calculate_distance(
        source_airport, row['latitude_deg'], row['longitude_deg']), axis=1)

    # https://www.geeksforgeeks.org/pandas/drop-rows-from-the-dataframe-based-on-certain-condition-applied-on-a-column/
    indices_to_drop = data[data['ident'] == source.upper()].index
    data = data.drop(indices_to_drop)
    data = data[data['distance_to'] <= area]
    return data


def choose_random_airport(data, sort):
    """
    Select 10 random airports from provided dataset.

    Args:
        data (pd.DataFrame): DataFrame of airports to sample from.
        sort (bool): If True, sort results by distance_to column; otherwise return unsorted.

    Returns:
        pd.DataFrame: DataFrame containing 10 randomly sampled airports.
    """
    df = data.sample(n=10)
    if sort:
        return df.sort_values('distance_to')
    else:
        return df


# FAST API
@app.get('/')
async def root():
    return {'message': 'Hello World'}


@app.get('/airport/{icao}')
async def airport_icao(icao: str):
    return get_airport(icao)


@app.get('/calculate/distance/{source}/{destination}')
async def calculate_source_destination(source: str, destination: str):
    result = calculate_distance(source=source, destination=destination)
    return {'source': source.upper(), 'destination': destination.upper(), 'result': result}


@app.get('/calculate/nearest/{source}/{area}')
async def calculate_nearest_airport(source: str, area: int):
    results_range = calculate_range(source, area).sort_values('distance_to')
    formatted_results = results_range.to_dict(orient='records')
    random_results = choose_random_airport(
        results_range, True).to_dict(orient='records')
    print(pd.DataFrame(formatted_results))
    print("------------------Random-------------------")
    print(pd.DataFrame(random_results))
    return {'source': source.upper(), 'random': random_results, 'all': formatted_results}
