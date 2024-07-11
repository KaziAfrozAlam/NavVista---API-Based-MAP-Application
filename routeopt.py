import leafmap.kepler as leafmap
import geopandas as gpd
import geocoder
import pandas as pd
import requests
import polyline
from shapely.geometry import LineString
m = leafmap.Map(center=[51.52738771088042, -0.15355043538426116], zoom=14, height=600)
m

df = pd.DataFrame({'longitude': [-0.15355043538426116, -0.1734286299198402] , 'latitude': [51.52738771088042, 51.50723029796882]})
geometry = gpd.GeoSeries.from_xy(df.longitude, df.latitude, crs="EPSG:4326")
geometry

m = leafmap.Map(center=[51.52738771088042, -0.15355043538426116], zoom=8, height=600)
m.add_gdf(geometry, "Points")
m

a = LineString([
          [
            -0.14594972886106916,
            51.52894559042994
          ],
          [
            -0.15129551682267106,
            51.528032855631494
          ],
          [
            -0.15160535880559678,
            51.52845341849624
          ],
          [
            -0.1523200326853953,
            51.52888527901317
          ],
          [
            -0.15306815191993906,
            51.529085073160246
          ],
          [
            -0.15416644905539556,
            51.52906946502597
          ],
          [
            -0.15542601537725886,
            51.52852049779611
          ],
          [
            -0.15592220416849045,
            51.52778058446981
          ],
          [
            -0.15588035911886777,
            51.52728077227175
          ],
          [
            -0.15533231695596328,
            51.52663527065718
          ],
          [
            -0.15462029969279456,
            51.5262980383138
          ],
          [
            -0.15362806237664017,
            51.52616485014991
          ],
          [
            -0.15276108049147297,
            51.526267843705796
          ],
          [
            -0.1518908002990429,
            51.52661042402386
          ],
          [
            -0.151368460601077,
            51.52714885220857
          ],
          [
            -0.15122574843908865,
            51.5276024316164
          ],
          [
            -0.15131261295630338,
            51.52804851126257
          ]
        ])
a

a = gpd.GeoSeries(a, crs='4326')
m = leafmap.Map(center=[51.52738771088042, -0.15355043538426116], zoom=8, height=1000, widescreen=False)
m.add_gdf(a, "Linestring Layer")
m

g = geocoder.arcgis('London, Tower Bridge Rd, London SE1 2UP')
latlon = g.lat, g.lng
print(latlon)

df = pd.DataFrame({'longitude': [latlon[1]] , 'latitude': [latlon[0]]})
geometry = gpd.GeoSeries.from_xy(df.longitude, df.latitude , crs="EPSG:4326")
m = leafmap.Map(center=[51.52738771088042, -0.15355043538426116], zoom=12, height=1000, widescreen=False)
m.add_gdf(geometry, "Points")
m

df= pd.read_csv('open_pubs.csv')
df = df.iloc[:300,:]
df['latitude'] = pd.to_numeric(df['latitude'])
df['longitude'] = pd.to_numeric(df['longitude'])
df.head()

df = pd.DataFrame({'longitude': df.longitude , 'latitude': df.latitude})
geometry = gpd.GeoSeries.from_xy(df.longitude, df.latitude , crs="EPSG:4326")
m = leafmap.Map(center=[51.52738771088042, -0.15355043538426116], zoom=12, height=1000, widescreen=False)
m.add_gdf(geometry, "Points")
m

# api-endpoint
url = "https://router.project-osrm.org/route/v1/driving/13.388860,52.517037;13.397634,52.529407;13.428555,52.523219?overview=full"



# sending get request and saving the response as response object
r = requests.get(url )

# extracting data in json format
data = r.json()
encoded_polyline = data['routes'][0]['geometry']
encoded_polyline

decoded_polyline = polyline.decode(encoded_polyline, 5)
decoded_polyline = [t[::-1] for t in decoded_polyline]
decoded_polyline = gpd.GeoSeries(LineString(decoded_polyline[::-1]), crs='4326')
# geometry = gpd.GeoSeries.from_xy(decoded_polyline_points.longitude, decoded_polyline_points.latitude , crs="EPSG:4326")
m = leafmap.Map(center=[51.52738771088042, -0.15355043538426116], zoom=12, height=1000, widescreen=False)
m.add_gdf(decoded_polyline, "Points")
m

def main(path):
  url = ''
  df= pd.read_csv(path)
  df = df.iloc[:300,:]
  df['latitude'] = pd.to_numeric(df['latitude'])
  df['longitude'] = pd.to_numeric(df['longitude'])
  for i in range(len(df)):
    url += str(df['longitude'][i]) + ',' + str(df['latitude'][i]) + ';'
  url = f"https://router.project-osrm.org/route/v1/driving/{url[:-2]}?overview=full"
  r = requests.get(url )
  data = r.json()
  encoded_polyline = data['routes'][0]['geometry']
  decoded_polyline = polyline.decode(encoded_polyline, 5)
  decoded_polyline = [t[::-1] for t in decoded_polyline]
  decoded_polyline = gpd.GeoSeries(LineString(decoded_polyline[::-1]), crs='4326')
  return decoded_polyline
route = main('open_pubs.csv')
route

m = leafmap.Map(center=[51.52738771088042, -0.15355043538426116], zoom=12, height=600, widescreen=False)
m.add_gdf(route, "route")
m