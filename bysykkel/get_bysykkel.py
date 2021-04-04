import requests
import datetime
import folium
import webbrowser
import os

def get_station_information():
    response = requests.get("https://gbfs.urbansharing.com/oslobysykkel.no/station_information.json")
    if not response.ok:
        raise ValueError("Something went wrong when querying the station infrmation API")
    return response.json()


def get_station_status():
    response = requests.get("https://gbfs.urbansharing.com/oslobysykkel.no/station_status.json")
    if not response.ok:
        raise ValueError("Something went wrong when querying the station status API")
    return response.json()


def merge_station_data():
    station_information = get_station_information()
    station_status = get_station_status()
    last_updated_station_information = datetime.datetime.utcfromtimestamp(station_information['last_updated'])
    last_updated_station_status = datetime.datetime.utcfromtimestamp(station_status['last_updated'])
    station_information_data = station_information['data']['stations']
    station_status_data = station_status['data']['stations']

    merged_info = {}
    for data in station_information_data:
        merged_info[data['station_id']] = data

    for data in station_status_data:
        station_id = data['station_id']
        merged_info[station_id] = merged_info[station_id] | data

    return merged_info, last_updated_station_information, last_updated_station_status


def create_map(citybikes_stations) -> folium.Map:
    map_types = ['Open Street Map', 'Stamen Terrain', 'Stamen Terrain', 'Stamen Toner', 'Stamen Watercolor', 'CartoDB Positron', 'CartoDB Dark_Matter']

    citybikes_map = folium.Map(location=[59.9, 10.75], zoom_start=12)
    for station_id, station_info in citybikes_stations.items():
        try:
            folium.Marker(location=[station_info['lat'], station_info['lon']],
                          popup=f"Last updated {datetime.datetime.utcfromtimestamp(station_info['last_reported'])},  \n"
                                f"broken bikes: {station_info['capacity'] - (station_info['num_docks_available']+ station_info['num_bikes_available'])}",
                          tooltip=f"{station_info['name']}: {str(station_info['num_bikes_available'])}/{str(station_info['capacity'])}").add_to(citybikes_map)

        except Exception as e:
            print(f"ups: {e}")

    for map_type in map_types:
        folium.raster_layers.TileLayer(map_type).add_to(citybikes_map)

    folium.LayerControl().add_to(citybikes_map)

    return citybikes_map


def runner():
    merged_info, last_updated_station_information, last_updated_station_information = merge_station_data()
    m = create_map(merged_info)
    base = os.getcwd()
    map_name = 'byskkel.html'
    save_path = os.path.join(base, f'maps\{map_name}')
    m.save(save_path)
    new = 2
    webbrowser.open(save_path, new=new)


if __name__ == 'main':
    print(f'running {__name__}')
    # last_updated, fest = clean_station_data()



