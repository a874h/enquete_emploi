# -*- coding: utf-8 -*-
"""
Cartographic  functions for enquete emploi data

Author: A.Hazan

schema: see queries.py

Refs:        
		http://python-visualization.github.io/folium/quickstart.html#Choropleth-maps
		https://perso.esiee.fr/~courivad/Python/15-geo.html
"""

import sqlite3
import folium
import pandas as pd

import queries
import cfg

def dashboard():
	"""
	check overleaf: Meeting_13_nov:Exploiting EE 
	check!!: file nb, people nb.
	nb people: check unique id. present in 181,182,183,184 ??
	nb employed
    per employment categ
	"""
	pass
	

def test_map_choropleth_employed_from_sql():
    """
    """
    fname_db="{}/emploi.db".format(cfg.ROUNT_MOUNT+cfg.ROOT)
    con = sqlite3.connect(fname_db)
	map_choropleth_employed_from_sql(con,fname_out='fig/choropleth.html')
	con.close()

def map_choropleth_employed_from_sql(con,fname_out='fig/choropleth.html'):	
	"""
    compute and save choropleth map.  

	data:
		https://www.data.gouv.fr/fr/datasets/contours-des-departements-francais-issus-d-openstreetmap/
		https://github.com/gregoiredavid/france-geojson
	"""	  
    # get nb of employed per departement
	c = queries.get_employed_count_by_dep_from_sql(con)
    con.close()
    # create map
    coords = (48.8398094,2.5840685)
    m = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=6)
    # add choropleth
    folium.Choropleth(
        geo_data= 'data/departements.geojson',
        name='nb employed (enquete emploi 2018)',
        data=c,
        columns=['State', 'Unemployment'],
        key_on='feature.properties.code',
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='nb employed'
    ).add_to(m)
    folium.LayerControl().add_to(m) 
    m.save(outfile=fname_out)
