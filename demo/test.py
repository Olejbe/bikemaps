import folium
from folium import plugins
import ipywidgets
import geocoder
import geopy
import numpy as np
import pandas as pd
from vega_datasets import data as vds
import os
import webbrowser

m = folium.Map()

#------------saves function to location

"""
map_variable.add_child(folium.LatLngPopup()) -> gives lat and lon when clicking the map. 
"""


def base_map() -> folium.Map:
    """
    Creates a base Map.
    """
    return folium.Map()


def base_map_with_scale() -> folium.Map:
    """
    Adds distance scale to the map.
    """
    return folium.Map(control_scale=True)


def base_map_with_different_layout():
    """
    different types of maps, set the attirbute tiles in the Map class to one of theese.
    1. Stamen Terrain
    2. Stamen Toner
    3. Stamen Watercolor
    4. CartoDB positron
    5. CartoDB Dark_Matter
    :return:
    """
    return folium.Map(control_scale=True, tiles='CartoDB Dark_Matter')


def base_map_with_layers():
    """
    We can add layers to the map and they will be available in the map for selection.
    :return:
    """
    map_layer_control = folium.Map(location=[38, -98], zoom_start=4)

    folium.raster_layers.TileLayer('Open Street Map').add_to(map_layer_control)
    folium.raster_layers.TileLayer('Stamen Terrain').add_to(map_layer_control)
    folium.raster_layers.TileLayer('Stamen Toner').add_to(map_layer_control)
    folium.raster_layers.TileLayer('Stamen Watercolor').add_to(map_layer_control)
    folium.raster_layers.TileLayer('CartoDB Positron').add_to(map_layer_control)
    folium.raster_layers.TileLayer('CartoDB Dark_Matter').add_to(map_layer_control)

    folium.LayerControl().add_to(map_layer_control)

    # Optional Minimap to bottom left corner
    minimap = plugins.MiniMap(toggle_display=True)
    map_layer_control.add_child(minimap)

    return map_layer_control


def create_multiple_pointers_1():
    # fetch data using vega_datasets
    airports = vds.airports()
    airports = airports[:25]

    # create map
    map_airports = folium.Map(location=[38, -98], zoom_start=4)
    for (index, row) in airports.iterrows():
        try:
            folium.Marker(location=[row.loc['latitude'], row.loc['longitude']], popup=row.loc['name'] + '' + row.loc['city']
                                                                                      + '' + row.loc['state'],
                      tooltip='click!').add_to(map_airports)
        except Exception:
            print("ups")

    return map_airports


def create_multiple_pointers_2():
    """
    Uses the dataframe built in apply function.
    This is faster and should be used for large datasets.
    """
    airports = vds.airports()
    airports = airports[:25]
    map_airports_2 = folium.Map(location=[38, -98], zoom_start=4)
    airports.apply(lambda row: folium.Marker(location=[row['latitude'], row['longitude']], popup=row['name'])
                   .add_to(map_airports_2), axis=1)

    return map_airports_2


def testing_with_geo_json():
    map_with_geo = folium.Map(location=[59.928522, 10.715429], zoom_start=6)
    path = os.path.join(os.getcwd(), f'demo\geojson_data\kommuner_komprimert.json')
    print(path)
    geo = folium.GeoJson(path).add_to(map_with_geo)
    folium.GeoJsonTooltip(fields=['lokalid']).add_to(geo)
    folium.LayerControl().add_to(map_with_geo)
    return map_with_geo

def testing_with_geo_json_1_entry():
    map_with_geo = folium.Map(location=[59.928522, 10.715429], zoom_start=6)
    path = os.path.join(os.getcwd(), f'demo\geojson_data\one_kommune.json')
    print(path)
    geo = folium.GeoJson(path).add_to(map_with_geo)
    folium.GeoJsonTooltip(fields=['navn']).add_to(geo)
    folium.LayerControl().add_to(map_with_geo)
    return map_with_geo


def runner():
    m = testing_with_geo_json_1_entry()
    base = os.getcwd()
    map_name = 'demo.html'
    save_path = os.path.join(base, f'maps\{map_name}')
    m.save(save_path)

    new = 2
    webbrowser.open(save_path, new=new)






# TODO Check out the extension geocoder.osm functionality.

"""
Apparantly the geocoder does an API lookup on address. 
"""


