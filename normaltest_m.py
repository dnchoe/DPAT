# -*- coding: utf-8 -*-

from numpy.random import seed
from numpy.random import randn
from scipy.stats import anderson
    
def normal_test(df, parameter='na'):
    """
    Args:
        df (dataframe): test table
        parameter: specific test parameter
    Returns:
        boolean: normal test result.
    """
    
    # parameter should be string type    
    if parameter=='na':
        data = df
    else: 
        data = df[parameter]
    
    # normality test
    result = anderson(data)
    #print(parameter+' Statistic: %.3f' % result.statistic)
    
    sl, cv = result.significance_level[2], result.critical_values[2]
    if result.statistic < cv:
        #print('%.3f: %.3f, data looks normal (fail to reject H0)' % (sl, cv))
        return True
    else:
        #print('%.3f: %.3f, data does not look normal (reject H0)' % (sl, cv))
        return False