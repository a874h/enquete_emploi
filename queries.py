# -*- coding: utf-8 -*-
"""
Useful queries, enquete emploi data

Author: A.Hazan


schema:
 * DEP: Département du logement de résidence
 * DEPETA Code du département de l'établissement employeur (principal)
 * SEXE: 1: masculin 2: feminin
 * AG: Âge détaillé en années révolues au 31 décembre
 * CSTOTPRM: Catégorie socioprofessionnelle (2 chiffres, niveau détaillé) de la personne de
référence du ménage
 * P: Profession principale des actifs occupés (PCS 4 chiffres)
 * NAFG017NPRM: Activité de l'établissement employeur (Nomenclature Agrégée 2008, 17 postes)
de la personne de référence du ménage
* ACTEU6: Statut d'activité au sens du Bureau International du Travail (BIT) selon l'interprétation
communautaire (6 postes). Vide: Sans objet (ACTEU non renseigné, individus de 15 ans et plus nécessairement non pondérés)
	1 Actif occupé; 3 Chômeur PSERE (Population sans Emploi à la Recherche d'un Emploi); 
	4 Autre chômeur BIT; 5 Etudiant, élève, stagiaire en formation (inactifs); 6 Autres inactifs (dont retraités)
* SPEFCD spécialité normalisée de la formation non formelle ;
* FORMFIN niveau détaillé de formation de la formation formelle ;
* DIPFIN niveau codé de la plus haute formation ;
* SPE version normalisée de la spécialité de la plus haute formation ;
* ANCCHOMM ancienneté au chomage en mois (si au chomage) ;
* DCHANTM durée au chomage avant de trouver l'emploi actuel ;

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
import pandas as pd

import cfg
import enquete_emploi.tools as ee_tools


def count_unique_id_concat(fname_):
    """
    count the number of unique IDENT in concatenated INDIV*.csv files
    """
    fname_db="{}/emploi_all.db".format(cfg.ROOT_2018)
    con = sqlite3.connect(fname_db)
    q = """ SELECT count(*) FROM (SELECT DISTINCT ident FROM indiv);"""
    return pd.read_sql_query(q, con)


def count_unique_id(con):
    """
    count the number of unique IDENT in 
    """
    q = """ SELECT count(*) FROM (SELECT DISTINCT ident FROM indiv);"""
    return pd.read_sql_query(q, con)

def test_get_employed_PCS_with_ROME():
    """
    """
    fname_db="{}/emploi_1.db".format(cfg.ROOT_2018)
    con = sqlite3.connect(fname_db)
    df = get_employed_PCS_with_ROME(con,filename="../jobagile/data/fap2009_pcs2003_romev3-1.xls")
    df['ROME'].apply( lambda x:x[0] ).value_counts()

def get_employed_PCS_with_ROME(con,filename,verbose=False):
    """
    same as get_employed_PCS_from_sql, with ROME code
    """
    # load PCS
    df_PCS = get_employed_PCS_from_sql(con)
    df_PCS= df_PCS.rename({'P':'PCS'},axis=1) 
    # load PCS2ROME
    df_ROME_PCS = ee_tools.get_PCS_ROME_table(filename)
    # join
    df_joined = join_ROME_codes(df_PCS,df_ROME_PCS)
    if verbose: 
        print(df_PCS.shape[0])
        print(df_joined.shape[0])
    return df_joined


def join_ROME_codes(df,df_ROME_PCS):
    """
    add a ROME code column from the PCS column
    """
    return pd.merge(df,df_ROME_PCS,how='inner')
    

def get_employed_PCS_from_sql(con):
    """
    get the PCS of employed responders
    CCONTR: Type de contrat de travail à l'entrée dans l'entreprise; 4=interim (p.35)
    P travail actuel	
    
    EEC2018_Dictionnaire des variables_Indiv(FPR)-1.pdf
    """
    q = """SELECT P,DEP,DEPETA,SEXE,CCONTR FROM indiv 
			WHERE ACTEU6=1  ;"""
    return pd.read_sql_query(q, con)        

def test_get_employed_count_by_dep_from_sql():
    """
    """
    fname_db="{}/emploi.db".format(cfg.ROOT_MOUNT+cfg.ROOT_2018)
    con = sqlite3.connect(fname_db)
    c = get_employed_count_by_dep_from_sql(con)
    con.close()
    c.plot(kind='bar')

def get_unenmployed_count_by_dep_from_sql(con):
    """
    """
    q="""select DEP as dep, count(*) AS nb_chom from indiv WHERE ANCCHOM>0 GROUP BY DEP;"""
    df_dep_chomage = pd.read_sql_query(q, con)
    q="""select DEP as dep, count(*) AS nb from indiv GROUP BY DEP;"""
    df_dep_all = pd.read_sql_query(q, con)
    return pd.merge(df_dep_all,df_dep_chomage,how="inner",on="dep" )

def get_employed_count_by_dep_from_sql(con, col_id='DEPETA',verbose=False):
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
	q = """SELECT {} FROM indiv 
			WHERE ACTEU6=1  ;""".format(col_id)  # use sqlalchemy instead
	df_dep_actif = pd.read_sql_query(q, con)
	if verbose: print(df_dep_actif.memory_usage())
	return df_dep_actif[col_id].value_counts()
	
	
def get_count_by_dep_pcs_with_ROME(con,filename):
    """
    TODO: create new table instead
    """
    # load PCS
    df_PCS = get_employed_count_by_dep_pcs_from_sql(con)
    df_PCS= df_PCS.rename({'P':'PCS'},axis=1) 
    # load PCS2ROME
    df_ROME_PCS = ee_tools.get_PCS_ROME_table(filename)
    # join
    df_joined = join_ROME_codes(df_PCS,df_ROME_PCS)   
    return df_joined    
    
def get_employed_by_dep_pcs_from_sql(con):
	"""
	get employed persons data 
	
	input:
	------
	con: sql connection
	
	output:
	-------
	pandas.core.series.Series
	indexed by departement.
	
	"""
	q = """SELECT DEPETA, P,SEXE,ZUS  FROM indiv 
			WHERE ACTEU6=1 
             ;"""
	return pd.read_sql_query(q, con)
        
    
def get_employed_count_by_dep_pcs_from_sql(con):
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
	q = """SELECT DEPETA, P,count(*) as count FROM indiv 
			WHERE ACTEU6=1 
            GROUP BY DEPETA, P
             ;"""
	return pd.read_sql_query(q, con)
	
def get_employed_count_by_dep_pcs_with_ROME(con,filename):
    """
    TODO: create new table instead
    """
    # load PCS
    df_PCS = get_employed_count_by_dep_pcs_from_sql(con)
    df_PCS= df_PCS.rename({'P':'PCS'},axis=1) 
    # load PCS2ROME
    df_ROME_PCS = ee_tools.get_PCS_ROME_table(filename)
    # join
    df_joined = join_ROME_codes(df_PCS,df_ROME_PCS)   
    return df_joined
   
    
    
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
	
