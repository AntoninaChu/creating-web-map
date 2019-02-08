import folium
import optparse
import geopy

def parse_options():
    '''
    This function gives the ability to parse users information
    from command line.
    '''
    usage = ("usage: %prog [options] [arg1 [arg2 [... argN]]]\n"
            "The arguments are optional; if not given all movies will be marked."
            "\nIf there was no option; all movies will be marked.")
    parser = optparse.OptionParser(usage = usage)
    parser.add_option("-y", "--year", dest="year", action="store_true",
            help="Program will mark movies from specified year [default: off]")
    parser.add_option("-n", "--name", dest="name", action="store_true",
            help="Program will mark the movies with "
                "the selected name [default: off]")
    parser.add_option("-l", "--location", dest="location", action="store_true",
            help="Program will mark movies with selected location "
                "[default: off]")
    parser.set_defaults(year=False, name=False, location=False)
    opts, args = parser.parse_args()
    opts = vars(opts)
    for option in opts:
        if opts[option]:
            return option, args
    return "year", []

def get_year(line):
    '''
    This function process a string and returns a year, that is written in this
    string.
    '''
    for char in line:
        if char =="(" and line[line.index(char)+ 5] == ")":
            year = line[line.index(char)+1:line.index(char)+ 5]
            if year.isdigit():
                return year

def get_name(line):
    '''
    This function process a string and returns words written in the paws.
    '''
    name = ""
    for char in line[1:]:
        if char == '"':
            break
        name += char
    return name


def get_location(line):
    '''
    This function process a string and returns adress written in this string.
    '''
    location = " "
    start_index=0
    for char in line:
        if char == "}" or char == "\t":
            start_index = line.index(char)+1
        elif char == "(" and line[-2] == ")":
            end_index = line.index(char)
    try:
        check = end_index
    except UnboundLocalError:
        end_index = len(line)-1
    location = line[start_index:end_index].strip()
    return location

def get_comment(line):
    '''
    This function process a string and returns words written in the curly braces.
    '''
    index1 = 0
    index2 = 0
    for char in line:
        if char == "{":
            index1 = line.index(char) + 1
        if char == "}":
            index2 = line.index(char)
    return line[index1:index2]

def add_data_to_dict(data_to_mark, movie_location, movie_name, movie_year, movie_comment):
    '''
    This function adds data to dictionary.
    '''
    value = data_to_mark.setdefault(movie_location, list())
    value.append([movie_name, movie_year, movie_comment])
    data_to_mark[movie_location] = value
    return data_to_mark

def process_data(option, args):
    '''
    This function reads data, compare it with users options and writes sorted
    data to dictionary.
    '''
    line_num = 0
    data_to_mark = dict()
    with open("locations.list.txt", "r", errors="ignore") as text:
        for line in text.readlines()[:50]:
            line_num += 1
            if line_num > 14:
                try:
                    movie_name = get_name(line)
                    movie_location = get_location(line)
                    movie_year = get_year(line)
                    movie_comment = get_comment(line)
                    if args != []:
                        for i in args:
                            if option == "year" and movie_year == i:
                                data_to_mark = add_data_to_dict(data_to_mark,
                                        movie_location, movie_name,
                                        movie_year, movie_comment)
                            elif (option == "name") and (i in movie_name):
                                data_to_mark = add_data_to_dict(data_to_mark,
                                        movie_location, movie_name,
                                        movie_year, movie_comment)
                            elif option == "location" and movie_location == i:
                                data_to_mark = add_data_to_dict(data_to_mark,
                                        movie_location, movie_name,
                                        movie_year, movie_comment)
                    else:
                        data_to_mark = add_data_to_dict(data_to_mark,
                                        movie_location, movie_name,
                                        movie_year, movie_comment)
                except IndexError:
                    pass
    return data_to_mark

def get_lat_lon(movie_location):
    '''
    This function recieves adress and returns longitude and latitude on the
    map of this point.
    '''
    try:
        geolocator = geopy.geocoders.Nominatim(user_agent="Google Maps")
        location = geolocator.geocode(movie_location)
        return [location.latitude, location.longitude]
    except AttributeError:
        print("Problems with geocoding.")
        return 0

def create_map(data_to_mark):
    '''
    This function creates a map and layers with markers on that map.
    '''
    movie_map = folium.Map()
    fg_location = folium.FeatureGroup(name="cirkle markers with locations")
    fg_name = folium.FeatureGroup(name="Movie Names")
    fg_comments = folium.FeatureGroup(name="Movie Comments")
    for movie_location in data_to_mark:
        for movie_data in data_to_mark[movie_location]:
            if get_lat_lon(movie_location) != 0:
                fg_name.add_child(folium.Marker(location=get_lat_lon(movie_location),
                                            popup=movie_data[0],
                                            icon=folium.Icon()))
                fg_comments.add_child(folium.Marker(location=get_lat_lon(movie_location),
                                            popup=movie_data[2],
                                            icon=folium.Icon()))
                fg_location.add_child(folium.CircleMarker(location=get_lat_lon(movie_location),
                                                    radius=10,
                                                    fill_color="red",
                                                    color='red' ,
                                                    fill_opacity=0.5))
    movie_map.add_child(fg_name)
    movie_map.add_child(fg_comments)
    movie_map.add_child(fg_location)
    movie_map.add_child(folium.LayerControl())
    movie_map.save("Movie_Map.html")

def main():
    '''
    This function puts together all functions.
    '''
    option, args = parse_options()
    print(option, args)
    data_to_mark = process_data(option, args)
    print(data_to_mark)
    create_map(data_to_mark)
main()
