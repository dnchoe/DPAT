# -*- coding: utf-8 -*-

from sklearn.ensemble import IsolationForest
    
def tree(df, parameter):
    """
    Args:
        df (dataframe): test table
        parameter: specific test parameter
    Returns:
        boolean: normal test result.
    """
    
    x=df[parameter].values
    x=x.reshape(-1,1)
    
    isolation_forest = IsolationForest(n_estimators=100)
    isolation_forest.fit(x)
    
    anomaly_score = isolation_forest.decision_function(x)
    outlier = isolation_forest.predict(x)
    
    remain_tf=[True if i==1 else False for i in outlier]
    
    print(parameter)
    
    return remain_tf