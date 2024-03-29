"""
When executed, this script launches the web application
with initial map.
"""

import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import omegaconf
import folium
from typing import Union, List, Any
from init_map import Map
from get_routes import Journey


class MapApp():

    def __init__(
            self,
            params):
        """
        This initialises an App class with the base map
        ready to be launched
        """
        # initialise application
        self.app = dash.Dash(__name__)
        self.base_map_params = params.init_map
        self.route_params = params.route_params
        self.api_creds = params.api_cred

        # init start and end points to keep track of
        self.last_start = None
        self.last_end = None
        self.get_n_routes(0, params.points['start'], params.points['end'])

        self.setup_layout()
    
    def setup_layout(self):
        """
        This function sets up the structre of the dash
        page with headers, inputs/buttons, and output placeholder
        """
        self.app.layout = html.Div([
            html.H1(
                "Green Mapper",
                style={
                    'color': 'green',
                    'font-family': 'Open Sans, sans-serif',
                    'text-align': 'center'
                }
            ),

            html.Div(
                [
                    dcc.Input(
                        id='start-point',
                        type='text',
                        placeholder='From..', 
                        style={'display': 'block'}
                    ),
                    dcc.Input(
                        id='end-point',
                        type='text',
                        placeholder='To..',
                        style={'display': 'block'}
                    ),

                    # triggers route display
                    html.Button(
                        'Get route options',
                        id='get-routes-button',
                        style={'display': 'block'}
                    ),

                    # Route ID dropdown menu
                    dcc.Dropdown(
                        id='route-id-drop',
                        placeholder='Select route option'
                    ),
                ],
                style= {
                    'width': '22%',
                    'display': 'inline-block',
                    'vertical-align': 'top',
                    'padding-left': '1%',
                }
            ),

            html.Div(
                [html.Iframe(id='folium-map', width='100%', height='600px')],
                style= {
                    'padding-left': '2%',
                    'width': '50%',
                    'display': 'inline-block',
                    'padding-right': '2%',
                }
            ),

            html.Div(
                [
                    html.Div(id='route-details'),
                ],
                style = {
                    'width': '22%',
                    'display': 'inline-block',
                    'vertical-align': 'top',
                    'font-family': 'Open Sans, sans-serif',
                    'padding-right': '1%'
                }
            ),

        ])

        # callback for getting routes
        self.app.callback(
            Output('route-id-drop', 'options'),
            [Input('get-routes-button', 'n_clicks')],
            [
                dash.dependencies.State('start-point', 'value'),
                dash.dependencies.State('end-point', 'value')
            ]
        )(self.get_n_routes)

        # callback for plotting routes and updating info
        self.app.callback(
            [
                Output('folium-map', 'srcDoc'),
                Output('route-details', 'children')
            ],
            [Input('route-id-drop', 'value')],
        )(self.update_visuals)
    
    
    def get_routes(
            self,
            start_point: Union[str, tuple[str, str]],
            end_point: Union[str, tuple[str, str]],
        ) -> Journey:
        """
        This function takes a start and end point and 
        retrieves the routes from the TFL API
        """
        journey = Journey(
            points=(start_point, end_point),
            route_params = self.route_params,
            cred_file = self.api_creds
        )
        journey.retrieve_routes()
        journey.extract_route_info()

        return journey
    
    def get_n_routes(
            self,
            n_clicks: int,
            start_point: Union[str, tuple[str, str]],
            end_point: Union[str, tuple[str, str]],
        ) -> List[dict[str, Any]]:
        """
        Creates labels and value dictionary for route id dropdown menu
        based in the journey provided
        """
        if n_clicks is None:
            return []

        # if new route has been requested, retrieve route
        if start_point != self.last_start or end_point != self.last_end:
            self.journey = self.get_routes(start_point, end_point)
            # update latest requested route
            self.last_start = start_point
            self.last_end = end_point
        
        route_names = [
            {'label': f"{id+1} - {' - '.join(route.modes)}", 'value': id}
            for id, route in self.journey.routes.items()
        ]
        return route_names
    
    def update_route_map(
            self,
            route_id: int
        ) -> dash:
        """
        This function takes user specified inputs, and 
        then plots the retrived route
        """
        if route_id is not None:
            try:
                map = Map(self.base_map_params)
                map._plot_route(self.journey, int(route_id))
                # return html representation of folium map
                return map._repr_html_()
            except ValueError:
                return "Please enter a valid route ID"
        else:
            return dash.no_update
        
    def update_route_info(self, route_id: int) -> List:
        """
        This function updates the route information displayed in the app
        """
        route = self.journey.routes[int(route_id)]
        return [

            html.Div([
                html.Strong("Departure time: "),
                html.Div(
                    route.depart_time,
                    style={
                        'border': '1px solid #ccc',
                        'padding': '10px',
                        'margin-bottom': '10px'
                    }
                ),
            ]),
    
            html.Div([
                html.Strong("Arrival time: "),
                html.Div(
                    route.arrive_time,
                    style={
                        'border': '1px solid #ccc',
                        'padding': '10px',
                        'margin-bottom': '10px'
                    }
                )
            ]),

            html.Div([
                html.Strong('Journey time: '),
                html.Div(
                    f"{route.total_duration} minutes",
                    style={
                        'border': '1px solid #ccc',
                        'padding': '10px',
                        'margin-bottom': '10px'
                    }
                ),
            ]),

            html.Div([
                html.Strong('Instructions: '),
                dcc.Markdown(
                    route.print_summary,
                    style={
                        'border': '1px solid #ccc',
                        'padding': '10px',
                        'margin-bottom': '10px'
                    }
                ),
            ]),

            html.Div([
                html.Strong("Total emissions (gCO2e): "),
                html.Div(
                    route.total_co2,
                    style={
                        'border': '1px solid #ccc',
                        'padding': '10px',
                        'margin-bottom': '10px'
                    }
                ),
            ]),

            html.Div([
                html.Strong("Emissions savings (gC02e): "),
                html.Div(
                    route.co2_saving,
                    style={
                        'border': '1px solid #ccc',
                        'padding': '10px',
                        'margin-bottom': '10px'
                    }
                ),
            ])
 
        ]
    
    def update_visuals(self, route_id: int) -> tuple:
        """
        This wrapper function calls functions to update the map and
        summary details of the updated route id
        """
        map_src_doc = self.update_route_map(route_id)
        route_blocks = self.update_route_info(route_id)

        return map_src_doc, route_blocks

    def run(self):
        self.app.run_server(debug=True)

    
if __name__ == "__main__":
    params = omegaconf.OmegaConf.load('params.yml').default
    app = MapApp(params)
    app.run()