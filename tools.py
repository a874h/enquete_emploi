# -*- coding: utf-8 -*-
"""
Misc functions for enquete emploi data

Author: A.Hazan

"""
import pandas as pd



def get_PCS_ROME_table(filename="data/fap2009_pcs2003_romev3-1.xls"):
    """
    get the PCS code/ROME code correspondence table
    """
    df_dict = pd.read_excel(filename,sheet_name='Table', usecols = "C,D,E,G")
    df_dict.dropna(axis=0,inplace=True,subset=["PCS","ROME"])
    return df_dict
