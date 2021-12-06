# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from scipy.stats as stats

def Grubbs(df, parameter):
    """
    Args:
        df (dataframe): test table
        parameter: specific test parameter
    Returns:
        float: upper limit and lower limit
    """
    y = df[parameter]
    
    G_stat=1;G_cri=0;
    rm_l=[]

    while G_stat>G_cri:    

        y = y.drop(labels=rm_l)
        G_cri = calculate_critical_value(len(y), 0.05)

        avg_y = np.mean(y)
        abs_val_minus_avg = abs(y - avg_y)
        max_of_deviations = max(abs_val_minus_avg)
        rm_l = list(abs_val_minus_avg[abs_val_minus_avg==max_of_deviations].index)#add
        s = np.std(y)
        G_stat = max_of_deviations/s
    
    #calculateing limit to remove outliers
    r_mean=y.describe()['50%']
    r_std=(y.describe()['75%']-y.describe()['25%'])/1.35

    k=6
    ul,ll=r_mean+k*r_std, r_mean-k*r_std 
    
    return ul, ll

def calculate_critical_value(size, alpha):
    """Calculate the critical value with the formula given for example in
    https://en.wikipedia.org/wiki/Grubbs%27_test_for_outliers#Definition
    Args:
        ts (list or np.array): The timeseries to compute the critical value.
        alpha (float): The significance level.
    Returns:
        float: The critical value for this test.
    """
    t_dist = stats.t.ppf(1 - alpha / (2 * size), size - 2)
    numerator = (size - 1) * np.sqrt(np.square(t_dist))
    denominator = np.sqrt(size) * np.sqrt(size - 2 + np.square(t_dist))
    critical_value = numerator / denominator
    #print("Grubbs Critical Value: {}".format(critical_value))
    
    return critical_value

