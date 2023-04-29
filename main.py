import pandas
from gpx import add_wps
from flask import Flask, render_template, request, url_for
import folium
import gpxpy

app = Flask(__name__)


def create_gpx_file(filename, mapname, mapdescription):
	data = pandas.read_csv(filename)
	add_wps(data.iterrows(), mapname, mapdescription)


@app.route("/", methods=['GET', 'POST'])
def hello_world():
	# Générate map
	if request.method == 'POST':
		map = request.form.get('map')
		map = f'maps/{map}.gpx'
	else:
		map = f"maps/test.gpx"

	start_coords = (46.3306752, -0.4685824)
	folium_map = folium.Map(location=start_coords, zoom_start=14)

	with open(map, 'r', encoding='utf-8') as f:
		gpx = gpxpy.parse(f)

	for wp in gpx.waypoints:
		folium.Marker([wp.latitude, wp.longitude], popup=wp.name).add_to(folium_map)

	folium.Marker([46.8354, -121.7325], popup="Camp Muir").add_to(folium_map)

	return render_template('index.html', map=folium_map._repr_html_(), map_name=gpx.name,
						   map_description=gpx.description)


if __name__ == '__main__':
	app.run(debug=True)
