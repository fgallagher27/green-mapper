"""
When executed, this script launches the web application
with initial map.
"""

import folium
import dash
import omegaconf
from dash import html
from dash_core_components import Graph
from dash.dependencies import Output
from init_map import Map


class App():

    def __init__(self, base_map_params: dict):
        """
        This initialises an App class with the base map
        ready to be launched
        """
        # initialise base map
        self.map = Map(base_map_params).base_map
        self.title = "Green Mapper"

    def _launch(self):
        """
        Launches the Dash app
        """
        app = dash.Dash(__name__)

        app.layout = html.Div([
            doc.Grpah(id="map")
        ])
    
        @app.callback(
                Output("map", "figure"),
                []
        )(self.update_map)
        def _display_map(self):
            """
            converts map to a dash figure for display
            """
            return self.map.get_root().render()

if __name__ == "__main__":
    map_params = omegaconf.OmegaConf.load('params.yml').default.init_map
    app = App(map_params)
    app._launch()