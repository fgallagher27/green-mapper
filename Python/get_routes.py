"""
This script accesses the TFL API to retrieve
routes between two points based on current
transport network status
"""

import os
import requests
import omegaconf
import ast
from typing import List, Union

def get_start_end(file: str = "params.yml") -> tuple[Union[float, str], Union[float, str]]:
    """
    Extracts the starting and ending point of the journey from the
    parameter file `params.yml` and returns as a list.
    The points in `params.yml` should be either postcodes or 
    long/lat coordinates.
    """
    params = omegaconf.OmegaConf.load(file)
    return params.default.points.start, params.default.points.end


class Credentials():
    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key


def load_credentials(file: str) -> Credentials:
    """
    This function accesses the text file with
    the TFL API credentials and stores them in
    a Credentials container
    """
    with open(file, 'r') as file:
        lines = file.readlines()

    app_id = lines[0].replace(" ", "").replace("\n", "").split(':')[1]
    app_key = lines[1].replace(" ", "").replace("\n", "").split(':')[1]

    return Credentials(app_id, app_key)


class Leg():
    """
    Contains information about a route leg between two
    intermediate points based on the dictionary output
    from the TFL API journey planner
    """
    def __init__(self, leg_info: dict, compute_cost: bool = True, compute_env_cost: bool = True):
        self.duration = leg_info['duration']
        self.start_point_coord = [leg_info['departurePoint']['lat'], leg_info['departurePoint']['lon']]
        self.start_point_name = leg_info['departurePoint']['commonName']
        self.end_point_coord = [leg_info['arrivalPoint']['lat'], leg_info['arrivalPoint']['lon']]
        self.end_point_name = leg_info['arrivalPoint']['commonName']
    
        self.path = (
            [tuple(self.start_point_coord)] +
            [tuple(point) for point in ast.literal_eval(leg_info['path']['lineString'])] +
            [tuple(self.end_point_coord)]
        )

        self.mode = leg_info['mode']['name']
        self.line = leg_info['routeOptions'][0]['name']

        self.interchange_duration = leg_info.get('interChangeDuration', None)
        if leg_info.get('interChangePosition', None) == 'BEFORE':
            self.interchange_position = 'start'
        elif leg_info.get('interChangePosition', None) != '':
            self.interchange_position = 'end'
        else:
            self.interchange_position = None
        
        self.cost=None
        if compute_cost:
            self.cost = self._calc_cost(leg_info)
        
        self.co2_cost = None
        self.air_poll = None
        if compute_env_cost:
            self.co2_cost, self.air_poll = self._calc_env_cost(leg_info)
    
    def _calc_cost(self, leg_info: dict):
        return None
    
    def _calc_env_cost(selfs, leg_info: dict):
        return None, None   


class Route():
    """
    Contains summary information about a possible route between
    two points and a dictionary containing each leg as well
    """
    def __init__(self, route_info: dict, compute_total_cost: bool = True, compute_env_cost: bool = True):
        self.total_duration = route_info['duration']
        self.depart_date_time = route_info['startDateTime']
        self.arrive_date_time = route_info['arrivalDateTime']
        self.num_legs = len(route_info['legs'])

        # extract info by leg
        self.legs = {}
        for i in range(self.num_legs):
            self.legs[i] = Leg(route_info['legs'][i],compute_total_cost, compute_env_cost)

        # stitch leg paths to get total route path
        self.path = []
        for _, leg in self.legs.items():
            self.path.append(leg['path'])
        
        self.total_cost = None
        if compute_total_cost:
            self.total_cost = self._calc_total_cost()

        self.total_co2 = None
        self.total_air_poll = None
        if compute_env_cost:
            self.total_co2, self.total_air_poll = self._calc_total_env_cost()
    
    def _calc_total_cost(self) -> float:
        """
        Calculate the total cost of a journey in GBP
        """
        return None

    def _calc_total_env_cost(self) -> tuple[float, float]:
        return None, None
    
    def _get_modes(self) -> List[str]:
        """
        This function accesses the information on
        each leg and retrieves the modes used, returning
        a list of strings.
        Where the mode has a sub level, this is concatenated
        using a backslash as a seperator:
        i.e. tube/bakerloo"""
        modes = []
        for _, leg in self.legs.items():
            str = leg.mode + "/" + leg.line
            modes.append(str)
        return modes


class Journey():
    """
    Acts as a container for information relating
    to a given journey from one point to another
    """

    def __init__(
            self,
            points: tuple[Union[float, str], Union[float, str]],
            route_params: dict = {},
            cred_file: str = 'tfl_api.txt',
        ):
        """
        params:
            points: tuple containing the start and end point of the route
            route_params: dictionary containing other parameters to pass to API request
            cred_file: text file holding API access key and id information
        """

        # load credentials from a text file
        self.credentials = load_credentials(cred_file)
        self.start = points[0]
        self.end = points[1]
        self.route_params = route_params

        # build url query
        self.url = self._construct_route_url()
    
    def _construct_route_url(self) -> str:
        """
        This function uses the start and end points of the
        journey and api access tokens to construct the
        TFL API url call.
        Additional parameters allowed by the API call can be added to
        the parameter object passed to the class.
        """
        base_url = "https://api.tfl.gov.uk/Journey/JourneyResults/"
        points = f"{self.start}/to/{self.end}"
        credentials = f"?app_id={self.credentials.app_id}&app_key={self.credentials.app_key}"

        url = base_url + points + credentials
        for key, value in self.route_params.items():
            url += f"&{key}={value}"

        return url
    
    def retrieve_routes(self):
        """
        This function executes the API request using the TFL
        API and the constructed URL
        """
        response = requests.get(self.url)
        if response.status_code == 200:
            self.status = "Successful"
            self.full_content = response.json()
        else:
            self.status = f"Failed with status code: {response.status_code}"
            self.full_content = None

    def extract_route_info(self):
        """
        This function converts the JSON output of the API
        request to custom classes containing key information
        and can be used throughout the model
        """
        self.num_routes = len(self.full_content['journeys'])
        self.routes = {}
        for i in self.full_content:
            self.routes[i] = Route(self.full_content['journeys'][i])

    def __repr__(self):
        return f"Journey class from {self.start} to {self.end}"


def extract_start_end(points: List)-> tuple[List[float], List[float]]:
    """
    This function takes a list of lists of points and extracts the
    first and last coordinate pair as lists
    """
    return list(points[0][0]), list(points[-1][-1])

