import osmnx as ox
from geopy.geocoders import Nominatim
import seaborn as sns
import logging
logging.basicConfig(level=logging.INFO)
sns.set()


def extract_location_data(place: str):
    try:
        G = ox.graph_from_place([place], network_type="all", simplify=True)
        locator = Nominatim(user_agent="Geocoder")
        coordinates = locator.geocode([place])
        if coordinates:
            logging.info('Your location was found.')
            return G, coordinates
    except Exception:
        logging.error(
            'The location could not be found. Please try a different input')


def extract_location_meta(G):
    map_metadata = []
    for _, _, _, data in G.edges(keys=True, data=True):
        map_metadata.append(data)
    return map_metadata


def define_road_color(map_metadata):
    types = []
    for i in range(len(map_metadata)):
        types.append(map_metadata[i].get('highway'))
    elements = []
    for i in range(len(types)):
        if type(types[i]) == list:
            elements.append(types[i])
    for el in elements:
        types.remove(el)
    distinct_types = list(set(types))
    n_distincts = len(distinct_types)
    # color_list =sns.cubehelix_palette(n_distincts+1, start=2, rot=0.1, dark=0.1, light=.9, reverse=True).as_hex()
    color_list = sns.diverging_palette(
        255, 133, l=60, n=n_distincts, center="dark").as_hex()
    road_colors = []
    for item in map_metadata:
        if item["highway"] in distinct_types:
            color = color_list[distinct_types.index(item["highway"])]
        else:
            color = color_list[-1]
        road_colors.append(color)
    return road_colors


def define_road_width(map_metadata):
    # List to store linewidths
    road_widths = []
    for item in map_metadata:
        if "footway" in item["highway"]:
            linewidth = 0.75
        else:
            linewidth = 1.5
        road_widths.append(linewidth)
        return road_widths


def draw_map(G, place, coordinates, road_colors, road_widths, lat_side=0.025, lon_side=0.075):

    # Map Center
    latitude = coordinates.latitude
    longitude = coordinates.longitude

    # Focus boundaries
    north = latitude + lat_side
    south = latitude - lat_side
    east = longitude + lon_side
    west = longitude - lon_side

    # Draw Map
    fig, ax = ox.plot_graph(
        G,
        node_size=0,
        bbox=(north, south, east, west),
        margin=0,
        fig_height=40,
        fig_width=90,
        dpi=400,
        bgcolor="#000000",
        save=True,
        filename=place,
        file_format='jpg',
        edge_color=road_colors,
        edge_linewidth=road_widths,
        edge_alpha=1,
    )
