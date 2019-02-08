# creating-web-map
Module returns HTML file (Movie_Map.html)

This module creates a web map, that has three layers. On this map you will see markers with movie name, comments to this movie
and markers with location, where that movie was filmed. 
You can give some options from command line to choose movies, that you want to see on your map.
You can write a year and programm will show on map only movies, that were filmed that year.
You also have ability to choose movies by name or location, where it was filmed.
To find film and locations this programm uses a file with all that data(locations.list.txt)

To see how to use program you must to write this in your command line:
web_map.py --help

Map is created using folium module.
