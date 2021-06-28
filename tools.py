# -*- coding: utf-8 -*-
"""
Misc functions for enquete emploi data

Author: A.Hazan

"""
import pandas as pd




def get_PCS_ROME_table(filename="data/fap2009_pcs2003_romev3-1.xls"):
    """
    get the 1-way PCS code/ROME code correspondence table
    in order to convert from PCS to code ROME (NOT THE REVERSE!)
    
    
    source = https://dares.travail-emploi.gouv.fr/donnees/la-nomenclature-des-familles-professionnelles-fap-2009
                   https://www.pole-emploi.org/opendata/repertoire-operationnel-des-meti.html?type=article
                   
    """
    df_dict = pd.read_excel(filename,sheet_name='Table', usecols = "C,D,E,G")
    df_dict.dropna(axis=0,inplace=True,subset=["PCS","ROME"])
    return df_dict
