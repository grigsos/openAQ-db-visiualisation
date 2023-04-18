import pandas as pd
import plotly.express as px
import plotly.io as pio
from typing import List, Dict, Any
from constants import get_s3_bucket


def plot_item(items: List[Dict[str, Any]], param: str) -> None:
    
    filtered_items = [item for item in items if 'average' in item and 'latitude' in item and 'longitude' in item]

    readings: List[float] = [item['average'] for item in filtered_items]
    latitudes: List[float] = [item['latitude'] for item in filtered_items]
    longitudes: List[float] = [item['longitude'] for item in filtered_items]
    
    min_reading: float = min(readings)
    max_reading: float = max(readings)
    reading_range: float = max_reading - min_reading
    
    normalized_radius: List[float] = [(reading - min_reading) / reading_range for reading in readings]
    radius: List[float] = [r * reading_range + 1 for r in normalized_radius]


    fig = px.density_mapbox(lat=latitudes, lon=longitudes, z=radius, radius=40, opacity=0.7)
    fig.update_layout(mapbox_style='open-street-map', mapbox_center_lon=4.4699, mapbox_center_lat=50.5039, mapbox_zoom=6)

    image_bytes = pio.to_image(fig, format='png')
    parameterName = param + ".png"
    
    bucket=get_s3_bucket()
    bucket.put_object(Body=image_bytes, Key=parameterName)

    return None