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

Refs:
* DICTIONNAIRE DES VARIABLES DU FICHIER DE DONNÉES INDIVIDUELLES DE L’ENQUÊTE EMPLOI, 2017.
* https://quanti.hypotheses.org/1871
"""

import folium
import pandas as pd
from io import StringIO

import cfg

def map_choropleth_contract_location_from_csv(filename,colnames=['DEP','DEPETA','AG', 'SEXE','CSTOTPRM','NAFG017NPRM']):	
	"""
    compute choropleth map.
    
	http://python-visualization.github.io/folium/quickstart.html#Choropleth-maps
	https://perso.esiee.fr/~courivad/Python/15-geo.html
	"""	
	pass
    
	df = pd.read_csv(filename)
	df = df[colnames]
