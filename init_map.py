"""
This file contains the code to build an
interactive folium map and plot journeys
"""

import folium
from typing import List
from get_routes import Journey, extract_start_end

class Map(folium.Map):
    """
    This class contains a folium map.
    A journey is then used to plot start, end points
    and the jounrey legs onto the map.
    """

    def __init__(
            self,
            map_params: dict,
        ):
        # initialise map with base parameters
        super().__init__(**map_params)

        # set colour attribute map
        # hex codes from https://blog.tfl.gov.uk/2022/12/22/digital-colour-standard/
        self.colour_map = {
            'walking': 'grey',
            'cycle': 'light green',
            'tube/Bakerloo': '#B26300',
            'tube/Central': '#DC241F',
            'tube/Circle': '#FFC80A',
            'tube/District': '#007D32',
            'tube/Hammersmith & City': '#F589A6',
            'tube/Jubilee': '#838D93',
            'tube/Metropolitan': '#9B0058',
            'tube/Northern': '#000000',
            'tube/Piccadily': '#0019A8',
            'tube/Victoria': '#039BE5',
            'tube/Waterloo & City': '#76D0BD',
            'elizabeth-line': "#60399E",
            'national-rail': "#BF40BF",
            'overground': '#FA7B05',
            'dlr': '#00AFAD',
            'bus': '#DC241F',
            'river': '#039BE5',
            'cablecar': '#DC241F',
            'tram': '#5FB526'
        }
    
    def _plot_route(self, journey: Journey, route_id: float):
        """
        This function takes a journey class and overlays the route specified
        by route id onto the base map
        """

        # assert route_id is a valid id
        msg = (
            f"Route id should be an integer value no larger than the maximum number of routes:"
            f"{journey.num_routes}"
        )
        assert route_id <= journey.num_routes - 1, msg
        
        self.path = journey.routes[route_id].path
        self.start_point, self.end_point = extract_start_end(self.path)
        self.start_name = journey.routes[route_id].legs[0].start_point_name
        self.end_name = journey.routes[route_id].legs[journey.routes[route_id].num_legs - 1].end_point_name

        # recentre map on start point
        self.location = self.start_point
        # add start and end points of route
        folium.Marker(
            location=self.start_point,
            popup=f'Start Point:<br>{self.start_name}<br>{self.start_point}'
        ).add_to(self)

        folium.Marker(
            location=self.end_point,
            popup=f'End Point:<br>{self.end_name}<br>{self.end_point}'
        ).add_to(self)
        
        modes = journey.routes[route_id]._get_modes()
        lines_col_zip = match_line_to_col(self.path, modes, self.colour_map)
        # add each leg to map
        for line, colour in lines_col_zip:
            folium.PolyLine(
                locations=line,
                color=colour,
                weight = 8,
                opacity=1,
            ).add_to(self)

    def _repr_html_(self):
        return self.get_root().render()


def match_line_to_col(lines: List, modes: List, col_map:dict) -> zip:
    """
    This function takes a list of lines and corresponding
    list of mode/types and returns the colour to plot each
    line in according to an attribute map
    """
    colours = []
    for line, mode in zip(lines, modes):
        colours.append(col_map[mode])
    mapped_lines = zip(lines, colours)
    return mapped_lines