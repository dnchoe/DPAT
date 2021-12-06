# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import scipy.stats as stats
import collections
import matplotlib.pyplot as plt
from scipy import optimize #yeo jhonson transformation
from sklearn.ensemble import IsolationForest

#import defined functions from other files
from aec_dpat_m import *
from grubbs_m import *
from yeojohnson_m import *
from normaltest_m import *
from tree_m import *

def r_dpat(df, parameter_list=['para1', 'para2', 'para3', 'para4'], method):
    
    """argument
    #1 'parameter_list' argument: default value is ['para1', 'para2', 'para3', 'para4']
    #2 'method' argument: specify one of the following three methods ['tree', 'aec_dpat']
    """
    
    result=dict()
    wafer_l=list(df.wafer_id.unique())
    print(df.shape)
    
    #per parameter
    for parameter in parameter_list:
        print(parameter)
        remain_l=[]
                
        #for each wafer
        for wafer in wafer_l:
            print(wafer)
            remain_tf=[]
            
            normal_result1=normal_test(df[df.wafer_id==wafer], parameter)

            #first apply grubbs
            ul, ll = Grubbs(df[df.wafer_id==wafer], parameter)
            remain_tf=remain(df[df.wafer_id==wafer], parameter, ul, ll)
            normal_result2=normal_test(df[df.wafer_id==wafer][remain_tf], parameter)

            if normal_result1==True:
                None
            elif normal_result2==True:
                None
            else: # elif  normal_result2==False:
                # if false, apply johnson
                data, lamb=yeo_johnson(df[df.wafer_id==wafer], parameter)
                # johnson normal -> Grubbs
                normal_result3=normal_test2(data) # is it possible?

                if normal_result3==True:
                    #apply grubb hubs
                    ul, ll = Grubbs(data, parameter)
                    remain_tf=remain(data, parameter, ul, ll)

                else: # when normal_result3==False
                    #apply AEC PAT
                    if method=='aec_dpat':
                        remain_tf=aec_dpat(df[df.wafer_id==wafer], parameter)
                    #apply Steve method
                    elif method=='tree':
                        remain_tf=tree(df[df.wafer_id==wafer], parameter)
                    #apply article method
            
            remain_l.extend(remain_tf)
        
        col_name=parameter+'_'+method+'_dpat_pf'
        result[col_name]=remain_l
    
    result_df= pd.DataFrame.from_dict(result)
    result_df['wafer_id'] = df['wafer_id'].values
    result_df['die_id']= df['die_id'].values 
    
    return result_df

#Data cleansing
def cleaning(df):

    # column name change
    new_col=[i.split('.')[1] for i in list(df.columns)]
    new_col=[i.replace('%', '') for i in new_col]
    new_col=[i.replace('(', '') for i in new_col]
    new_col=[i.replace(')', '') for i in new_col]
    new_col=[i.replace(' ', '_') for i in new_col]
    df.columns=new_col

    # POR only
    df=df[(df.device=='POR')]
    # mo measure remove
    df=df[(df.pre_aoi_bin!=50)]

    # print: current status
    print("The number of Wafers : "+str(len(list(df.wafer_id.unique()))))
    print("The Quality Score Result : "+str(collections.Counter(df.quality_score)))

    # print: parameter histograms
    fig = plt.figure(figsize = (15,20))
    ax = fig.gca()
    df[['var1', 'var2', 'var3', 'var4', 'var5']].hist(ax=ax)
    
    return df

def remain(df, parameter, ul, ll):
    
    remain_tf=[(i<ul) and (i>ll) for i in df[parameter]]
    
    return remain_tf

def yeo_johnson(df, parameter):
    
    y = df[parameter]
    yt, lamb = yeojohnson(y)
    
    return yt, lamb

