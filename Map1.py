import folium
import pandas


tiles_list= [
    "OpenStreetMap",
    "CartoDB positron",
    "CartoDB dark_matter",
    "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
]

m = folium.Map(
    location=[37.759289, -122.442255],
    zoom_start=6,
    tiles="CartoDB positron"
)

from folium.plugins import MiniMap
MiniMap().add_to(m)


for t in tiles_list:
    if t.startswith("https:"):
        folium.TileLayer(
            tiles=t,
            attr="Esri",
            name= "Esri Satellite",
            overlay=False,
            control=True
        ).add_to(m)
    else:
        folium.TileLayer(t).add_to(m)


data = pandas.read_csv("mapping/volcanoes.txt")
data1 = pandas.read_csv("mapping/TouristPlaces.txt")
data2 = pandas.read_csv("mapping/WorldPopularPlaces.txt")

lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])

lat1 = list(data1["LAT"])
lon1 = list(data1["LON"])
name1 = list(data1["NAME"])

lat2 = list(data2["LAT"])
lon2 = list(data2["LON"])
name2 = list(data2["NAME"])

def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'
    
fgpp = folium.FeatureGroup(name="Popular places")

for lt2, ln2, name2 in zip(lat2, lon2, name2):
    fgpp.add_child(
        folium.Marker
        (location= [lt2, ln2],
         popup= f"{name2} Place",
         icon=folium.Icon(color='orange')
         )
    )


fgt = folium.FeatureGroup(name="Turistic")

for lt1, ln1, name1 in zip(lat1, lon1, name1):
    fgt.add_child(
        folium.Marker
        (location= [lt1, ln1],
         popup= f"{name1} Place",
         icon=folium.Icon(color='lightgreen')
         )
    )

folium.PolyLine( #Trazo de punto a punto
    locations=[[lat1[0], lon1[0]], [lat1[1], lon1[1]], [lat1[2], lon1[2]]],
    color="lightblue", weight=3, opacity=0.8
).add_to(m)


fgv = folium.FeatureGroup(name="Volcanoes")


for lt, ln, el in zip(lat, lon, elev):
    fgv.add_child(
        folium.CircleMarker
                 (location = [lt, ln], 
                  radius = 6,
                  popup = str(el)+" m",
                  fill_color = color_producer(el),
                  color = 'grey',
                  fill_opacity = 0.7
                 )
    )

fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=(open('mapping/world.json', 'r', 
                                       encoding='utf-8-sig').read()),
                                       style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000 
                                            else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
                                            else 'red'})) #with those line of code i added a range of population based on scale beetwen 10000000 or more using green, orange and red.

m.add_child(fgt)
m.add_child(fgv)
m.add_child(fgpp)
m.add_child(fgp)

m.add_child(folium.LayerControl())
m.save("mapping/Map1.html")