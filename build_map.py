"""
This script can be ran to generate a map of the London
public transport system. Each layer of the map corresponds
to a different transport networks and the layers are held
together as a class.

If run alone, this script builds the layers according to a
given build_map file, but does not construct the class.
"""

import os
import requests
import omegaconf
import geopandas as gpd


class Map():

    def __init__(self, map_data_yml: str = ''):
        """
        Initialises a map build
        """
        # verify map has been built correctly
        print("Verifying map build...")
        build_map_layers(map_data_yml)
        map_data = omegaconf.OmegaConf.load(map_data_yml)
        
        # Load in layers according to map_data
        self.dir = map_data.map_dir
        self.layers={}
        print("Loading map layers...")
        # TODO a progress tracker
        for layer in map_data.layers:
            if layer.file.endswith(".shp"):
                temp = gpd.read_file(os.path.join(self.dir, layer.file))
            elif layer.file.endswith(".tiff"):
                pass
            self.layers[layer] = temp
            setattr(self, layer.name, temp)


def build_map_layers(map_data_yml: str, overwrite_layers: bool = False):
    """
    This function builds a map of london with each transport
    network forming its own layers.
    """
    map_data = omegaconf.OmegaConf.load(map_data_yml)

    n_layers = len(map_data.layers)
    for i, layer in enumerate(map_data.layers):
        if os.path.exists(os.path.join(map_data.map_dir, layer.file)):
            print(f"{layer.name} layer already exists")
            if overwrite_layers:
                print(f"overwriting {layer.name} layer...")
                build_layer(layer, map_data.crs)
        else:
            build_layer(layer, map_data.crs)
        print(f"{layer.name} completed: {i} / {n_layers} completed")
    print(f"Building map from {map_data_yml} completed")


def build_layer(layer: dict, crs: str):
    pass

def download_zip_from_url(url: str, file_path: str):
    """
    This function downloads a zip file from a url and places into file_path

    Args:
        url (str): url address of the zip folder to download
        file_path (str): folder path to save the zip file to including the name of the zip

    """
    print("Downloading data...")
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    response = requests.get(url)

    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"File '{file_path}' downloaded successfully.")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")


def extract_zip(zip_file_path: str, extract_location: str):
    """
    This function extracts the contents of a zipfile to extract_location.
    """
    print(f"Extracting data from {zip_file_path}")
    try:
        if not os.path.isfile(zip_file_path):
            raise FileNotFoundError(f"The file '{zip_file_path}' does not exist.")
        
        # Create the extraction directory if it doesn't exist
        os.makedirs(extract_location, exist_ok=True)

        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_location)

        print(f"Successfully extracted {zip_file_path} to {extract_location}")

    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def download_data(url: str, folder: str, file: str, extract_location: str):
    """
    This function checks if the data has already been downloaded.
    If it has not, it downloads and extracts it.
    """
    if os.path.exists(os.path.join("data", "inputs", file)):
        print(f"{file} is already downloaded in the subdirectory 'data'")
    elif os.path.exists(folder):
        print(f"Extracting data from {folder}...")
        extract_zip(folder, extract_location)
    else:
        print(f"Downloading and extracting data from {url}...")
        download_zip_from_url(url, folder)
        extract_zip(folder, extract_location)

if __name__ == "__main__":
    build_map_layers('map_data.yml')