from tools import extract_location_data, extract_location_meta, define_road_color, define_road_width, draw_map
import argparse


parser = argparse.ArgumentParser(description="Mapper drawing procedure")
parser.add_argument("location", type=str,
                    help="The location that you are going to map")
parser.add_argument("--lat_side", type=float, default=0.025,
                    help="The map focus boundaries on latitude")
parser.add_argument("--lon_side", type=float, default=0.080,
                    help="The map focus boundaries on longitude")


args = parser.parse_args()

args.location = str(args.location)

if __name__ == "__main__":
    place = args.location
    print(place)
    print(type(place))
    G, coordinates = extract_location_data(place)
    map_metadata = extract_location_meta(G)
    road_colors = define_road_color(map_metadata)
    road_widths = define_road_width(map_metadata)
    draw_map(G, place, coordinates, road_colors,
             road_widths, args.lat_side, args.lon_side)
