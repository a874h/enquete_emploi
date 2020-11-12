"""
Cartographic  functions for enquete emploi data

Author: A.Hazan

schema:
 * DEP: Département du logement de résidence
 * DEPETA Code du département de l'établissement employeur (principal)
 * SEXE: 1: masculin 2: feminin
 * AG: Âge détaillé en années révolues au 31 décembre
 * CSTOTPRM: Catégorie socioprofessionnelle (2 chiffres, niveau détaillé) de la personne de
référence du ménage
 * NAFG017NPRM: Activité de l'établissement employeur (Nomenclature Agrégée 2008, 17 postes)
de la personne de référence du ménage
* ACTEU6: Statut d'activité au sens du Bureau International du Travail (BIT) selon l'interprétation
communautaire (6 postes). Vide: Sans objet (ACTEU non renseigné, individus de 15 ans et plus nécessairement non pondérés)
	1 Actif occupé; 3 Chômeur PSERE (Population sans Emploi à la Recherche d'un Emploi); 
	4 Autre chômeur BIT; 5 Etudiant, élève, stagiaire en formation (inactifs); 6 Autres inactifs (dont retraités)

Refs:
    * DICTIONNAIRE DES VARIABLES DU FICHIER DE DONNÉES INDIVIDUELLES DE L’ENQUÊTE EMPLOI, 2017.
    * https://quanti.hypotheses.org/1871

* put csv in sqlite3 ?
        $ sqlite3 emploi.db
        >.separator ';' 
        >.mode csv
        >.import INDIV181.csv indiv 
        >.import INDIV182.csv indiv --skip 1   #SQLite Release 3.32.!!!!

"""

import sqlite3
import folium
import pandas as pd
#from io import StringIO

import cfg



def test_get_employed_count_by_dep_from_sql():
	"""
	"""
    fname_db="{}/emploi.db".format(cfg.ROOT_MOUNT+cfg.ROOT_2018)
    con = sqlite3.connect(fname_db)
    c = get_employed_count_by_dep_from_sql(con)
    con.close()
	c.plot(kind='bar')

def get_employed_count_by_dep_from_sql(con,verbose=False):
	"""
	get the count of employed persons per departement.
	
	input:
	------
	con: sql connection
	
	output:
	-------
	pandas.core.series.Series
	indexed by departement.
	
	"""
	q = """SELECT dep FROM indiv 
			WHERE ACTEU6=1  ;"""
	df_dep_actif = pd.read_sql_query(q, con)
	if verbose: print(df_dep_actif.memory_usage())
	return df_dep_actif['DEP'].value_counts()
	
	
def get_employed_count_by_dep_from_csv(filename,colnames=['ACTEU6','DEP','DEPETA','AG', 'SEXE','CSTOTPRM',
												'NAFG017NPRM']):
	"""
	get the count of employed persons per departement.
	"""
	df = pd.read_csv(filename, sep=";", names = colnames)
	df = df[colnames]
	df_actif = df[df["ACTEU6"] ==1  ]
	#df = df.astype({'CSTOTPRM': 'int64'},errors='ignore')
	df_dep_actif = df['DEP']
	df_dep_actif.value_counts().plot(kind='bar')		
	

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
    
    refs:
		http://python-visualization.github.io/folium/quickstart.html#Choropleth-maps
		https://perso.esiee.fr/~courivad/Python/15-geo.html
	data:
		https://www.data.gouv.fr/fr/datasets/contours-des-departements-francais-issus-d-openstreetmap/
		https://github.com/gregoiredavid/france-geojson
	"""	  
    # get nb of employed per departement
	c = get_employed_count_by_dep_from_sql(con)
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
