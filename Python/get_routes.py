"""
This script accesses the TFL API to retrieve
routes between two points based on current
transport network status
"""

import os
import requests
import geopandas as gpd
from typing import List

def extract_route_info() -> gpd.GeoDataFrame:
    pass

def retrieve_route(points: List, credentials: List) -> List[str, str]:
    url = construct_route_url(points, credentials)

    response = requests.get(url)
    if response.status_code == 200:
        status = "Successful"
        content = response.text
    else:
        status = f"Failed with status code: {response.status_code}"
    
    return content, status


def construct_route_url(points: List, credentials: List) -> str:
    return f"https://api.tfl.gov.uk/Journey/JourneyResults/{points[0]}/to/{points[1]}?app_id={credentials.app_id}&app_key={credentials.app_key}"