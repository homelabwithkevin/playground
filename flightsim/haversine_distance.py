# Created with Claude Code
import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on Earth
    using the Haversine formula.
    
    Args:
        lat1, lon1: Latitude and longitude of point 1 (in degrees)
        lat2, lon2: Latitude and longitude of point 2 (in degrees)
    
    Returns:
        Distance in nautical miles
    """
    # Earth's radius in nautical miles
    R = 3440.07
    
    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Differences
    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad
    
    # Haversine formula
    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    
    return distance


# Example usage: Distance between JFK (New York) and LAX (Los Angeles)
if __name__ == "__main__":
    # JFK coordinates
    jfk_lat, jfk_lon = 40.6413, -73.7781

    kbos_lat, kbos_long = 42.36197, -71.0079
    target_lat, target_long = 42.025101, -70.838097

    
    # LAX coordinates
    lax_lat, lax_lon = 33.9425, -118.4081
    
    distance = haversine_distance(kbos_lat, kbos_long, target_lat, target_long)
    print(f"Distance between JFK and LAX: {distance:.2f} nautical miles")
