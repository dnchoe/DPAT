# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

def aec_dpat(df, parameter):
    """
    Args:
        df (dataframe): test table
        parameter: specific test parameter
    Returns:
        list of boolean: outlier(false)
    """
    y = df[parameter]

    med=y.describe()['50%']
    p99=np.quantile(y, 0.99)
    p1=np.quantile(y, 0.01)
    k=6

    ul=med+k*(p99-med)*0.43
    ll=med-k*(med-p1)*0.43
    
    remain_tf=[(i<ul) and (i>ll) for i in y]
    
    print(' ')
    print(parameter)
    print("UPPER:"+str(ul))
    print("LOWER:"+str(ll))
    
    return remain_tf