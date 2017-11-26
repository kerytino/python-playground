# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 18:17:16 2017
Useful functions in clusters analysis.
Specially kmeans clusters
@author: srodriguezl
"""
import pandas as pd

# 1
# Function to automatically generate a summary of the cluster
# Before running--> double check:
        # 1- Remove variables that you dont want to include in the summary
        # 2- Check variables types (df.dtypes) and correct them (df.variable.astype(....))
 
# df: dataframe
# Target: result of the cluster
# pasthSave: path to save the excel with the result
# includeCatNan: Add a column to indicate NaNs category
      
def Summary_function(df,Target,pathSave,includeCatNan = False):
    # Indentify object and bool variables and create dummy variables
    factorVar = df.select_dtypes(include=["object","bool"]).columns
    for i in factorVar:
        df_dummy = pd.get_dummies(df[i], prefix = i , dummy_na = includeCatNan) 
        df = pd.concat([df,df_dummy],axis = 1)
        df.drop(i,axis = 1,inplace = True)
        
    # Compute mean for every column ( for dummy column the mean represents percentage of samples in each category)
    summary = df.groupby(Target, as_index=False).mean()
    
    # Compute cluster distribution
    distrib = df.groupby(Target, as_index = False).size()
    summary["count"] = distrib
           
    # Save result
    summary.to_excel(pathSave + "SummaryCluster.xlsx",sheet_name="SummaryCluster",index = False)
    
    # return result to be explored
    return(summary)


# 2
# Elbow_criterion
from ggplot import *
from sklearn.cluster import KMeans
    
def Elbow_criterion(df,maxNumClusters):
    
    inertiaValues = []
    for i in range(1,maxNumClusters+1):
        model =  KMeans(n_clusters = i)
        inertia = model.fit(df).inertia_
        inertiaValues.append(inertia)             
    inertiaValuesdf = pd.DataFrame({"numclusters":list(range(1,maxNumClusters+1)), "inertia": inertiaValues})
    p = ggplot(aes(x="numclusters",y="inertia"),inertiaValuesdf) + geom_line() + xlab("Number of clusters K") + ylab("Distorsion") + ggtitle("Elbow curve")
    return(p)


# 3
# Silhouette_criterion
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
from ggplot import *

def Silhouette_criterion(df,maxNumClusters):
    silhouette = []
    for i in range(2,maxNumClusters+1):
        model =  KMeans(n_clusters = i)
        labels = model.fit(df).labels_
        silhouette.append(silhouette_score(df,labels, metric = "sqeuclidean")) # by default euclidean
    silhoValuesdf = pd.DataFrame({"numclusters":list(range(2,maxNumClusters+1)), "silhouette_score": silhouette})
    p = ggplot(aes(x="numclusters",y="silhouette_score"),silhoValuesdf) + geom_line() + xlab("Number of clusters K") + ylab("Silhouette score") + ggtitle("Silhouette curve")
    return(p)